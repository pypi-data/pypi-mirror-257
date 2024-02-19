import json
import pathlib

import pytest
from pytest_httpx import HTTPXMock

from reskyblock import Client

_AUCTIONS_DATA = (pathlib.Path(__file__).resolve().parents[0] / "data" / "auctions.json").read_text(encoding="utf-8")
_AUCTIONS_ENDED_DATA = (pathlib.Path(__file__).resolve().parents[0] / "data" / "auctions_ended.json").read_text(
    encoding="utf-8"
)
_BAZAAR_DATA = (pathlib.Path(__file__).resolve().parents[0] / "data" / "bazaar.json").read_text(encoding="utf-8")


@pytest.fixture
def client() -> Client:
    return Client()


def test_client() -> None:
    _ = Client()


def test_get_auctions(httpx_mock: HTTPXMock, client: Client) -> None:
    httpx_mock.add_response(json=json.loads(_AUCTIONS_DATA))

    client.get_auctions()


def test_get_auctions_ended(httpx_mock: HTTPXMock, client: Client) -> None:
    httpx_mock.add_response(json=json.loads(_AUCTIONS_ENDED_DATA))

    client.get_auctions_ended()


def test_get_bazaar(httpx_mock: HTTPXMock, client: Client) -> None:
    httpx_mock.add_response(json=json.loads(_BAZAAR_DATA))

    client.get_bazaar()


def test_continuous_update_auctions(httpx_mock: HTTPXMock, client: Client) -> None:
    httpx_mock.add_response(json=json.loads(_AUCTIONS_DATA))

    for auction in client.get_auctions_continuous():
        assert len(auction.auctions) == 1000
        break


def test_continuous_update_auctions_ended(httpx_mock: HTTPXMock, client: Client) -> None:
    httpx_mock.add_response(json=json.loads(_AUCTIONS_ENDED_DATA))

    for _ in client.get_auctions_ended_continuous():
        break


def test_continuous_update_bazaar(httpx_mock: HTTPXMock, client: Client) -> None:
    httpx_mock.add_response(json=json.loads(_BAZAAR_DATA))

    for _ in client.get_bazaar_continuous():
        break
