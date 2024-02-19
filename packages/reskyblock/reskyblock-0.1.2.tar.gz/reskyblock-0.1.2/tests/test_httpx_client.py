import pytest
from pytest_httpx import HTTPXMock

from reskyblock.http import HTTPXClient


@pytest.mark.parametrize("params", [None, {"a": "a", "b": "b"}])
def test_httpx_client(httpx_mock: HTTPXMock, params: dict[str, str] | None) -> None:
    httpx_mock.add_response()

    data = HTTPXClient().get("https://test_url", params=params)
    assert data == b""
