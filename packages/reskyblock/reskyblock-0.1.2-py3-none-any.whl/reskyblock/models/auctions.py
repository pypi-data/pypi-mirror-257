from __future__ import annotations

import msgspec

from reskyblock.nbt import DecodedNBT

__all__ = (
    "Auction",
    "Auctions",
    "Bid",
)


class Bid(msgspec.Struct):
    auction_id: str
    bidder: str
    profile_id: str
    amount: int
    timestamp: int


class Auctions(msgspec.Struct, rename="camel"):
    success: bool
    page: int
    total_pages: int
    total_auctions: int
    last_updated: int
    auctions: list[Auction]


class Auction(msgspec.Struct):
    """Represents an auction instance on the auction house"""

    start: int
    end: int
    item_name: str
    extra: str
    category: str
    tier: str
    starting_bid: int
    item_bytes: str
    claimed: bool
    highest_bid_amount: int
    last_updated: int
    bin: bool
    uuid: str
    auctioneer: str
    profile_id: str
    decoded_nbt: DecodedNBT | None = None
    command: str | None = None

    def __post_init__(self) -> None:
        self.decoded_nbt = DecodedNBT(raw_data=self.item_bytes)

        self.command = (
            f"/viewauction {self.uuid[:9]}-"
            f"{self.uuid[9:13]}-{self.uuid[13:17]}-"
            f"{self.uuid[17:21]}-{self.uuid[21:]}"
        )
