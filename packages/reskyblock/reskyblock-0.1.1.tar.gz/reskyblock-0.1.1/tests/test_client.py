import pytest

from reskyblock import Client


def test_client() -> None:
    with pytest.raises(NotImplementedError):
        _ = Client()
