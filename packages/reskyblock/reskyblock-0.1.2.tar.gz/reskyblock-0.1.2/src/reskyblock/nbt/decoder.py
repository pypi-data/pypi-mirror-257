"""NBT (Named Binary Tag) protocol decoder
This relies on the https://pypi.org/project/NBT/ library.
"""
import json as dum_json
from base64 import b64decode
from io import BytesIO
from typing import Any

import nbt
from msgspec import Struct

__all__ = ("DecodedNBT",)


def _decode_nbt(raw_data) -> Any:
    return nbt.nbt.NBTFile(fileobj=BytesIO(b64decode(raw_data)))[0][0]


class DecodedNBT(Struct):
    """Decoded NBT item data"""

    raw_data: str
    is_pet: bool = False
    skyblock_id: str = ""
    reforge: str | None = None
    dungeon_stars: int = 0
    hot_potato_count: int = 0
    rarity_upgrades: int = 0
    enchantments: list[str] = []
    art_of_war_count: int = 0
    gems: list[str] = []
    scrolls: list[str] = []

    def __post_init__(self) -> None:
        nbt_data = _decode_nbt(self.raw_data)
        ea = nbt_data["tag"]["ExtraAttributes"]

        self.skyblock_id = str(ea["id"]).replace("STARRED_", "")

        if self.skyblock_id == "PET":
            self.is_pet = True
            pet_info = dum_json.loads(ea["petInfo"].value)
            pet_type = pet_info["type"]
            self.skyblock_id = f"{pet_type}_PET"

        self.reforge = None if ea.get("modifier") is None else ea.get("modifier").value

        if ea.get("dungeon_item_level") is not None:
            self.dungeon_stars = ea.get("dungeon_item_level").value
        elif ea.get("upgrade_level") is not None:
            self.dungeon_stars = ea.get("upgrade_level").value
        else:
            self.dungeon_stars = 0

        self.hot_potato_count = 0 if ea.get("hot_potato_count") is None else int(ea.get("hot_potato_count").value)
        self.rarity_upgrades = 0 if ea.get("rarity_upgrades") is None else int(ea.get("rarity_upgrades").value)

        self.enchantments = []
        if ea.get("enchantments") is not None:
            for enchantment_tag in ea.get("enchantments").tags:
                self.enchantments.append(
                    "ENCHANTMENT_" + enchantment_tag.name.upper() + "_" + str(enchantment_tag.value)
                )

        self.art_of_war_count = 0
        if ea.get("art_of_war_count") is not None:
            self.art_of_war_count = int(ea.get("art_of_war_count").value)

        self.gems = []
        if ea.get("gems") is not None:
            self.gems = ea.get("gems").value

        self.scrolls = []
        if ea.get("ability_scroll") is not None:
            for scroll_tag in ea.get("ability_scroll").tags:
                self.scrolls.append(scroll_tag.value)
