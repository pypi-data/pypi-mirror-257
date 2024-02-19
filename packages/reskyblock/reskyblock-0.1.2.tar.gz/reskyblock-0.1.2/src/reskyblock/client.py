import logging
import time
from collections.abc import Callable, Iterator

from reskyblock.http import AbstractHTTPClient, HTTPXClient
from reskyblock.models import Auctions, AuctionsEnded, Bazaar
from reskyblock.serialization import AbstractJSONDecoder, MSGSpecDecoder
from reskyblock.urls import _prepare_auctions_ended_url, _prepare_auctions_url, _prepare_bazaar_url

type APIEndpoint = Auctions | AuctionsEnded | Bazaar
type APIEndpointGetter = Callable[[], APIEndpoint]

__all__ = ("Client",)


class Client:
    def __init__(self) -> None:
        self._http_client: AbstractHTTPClient = HTTPXClient()
        self._json_decoder: AbstractJSONDecoder = MSGSpecDecoder()
        self._auctions_last_updated: int = 0
        self._auctions_ended_last_updated: int = 0
        self._bazaar_last_updated: int = 0

    def get_auctions(self, page: int = 0) -> Auctions:
        """Get a single page of active auctions"""
        resp_bytes = self._http_client.get(url=_prepare_auctions_url(page))
        auctions = self._json_decoder.serialize(resp_bytes, Auctions)
        self._auctions_last_updated = auctions.last_updated
        return auctions

    def get_auctions_ended(self) -> AuctionsEnded:
        """Get ended auctions"""
        resp_bytes = self._http_client.get(url=_prepare_auctions_ended_url())
        auctions_ended = self._json_decoder.serialize(resp_bytes, AuctionsEnded)
        self._auctions_ended_last_updated = auctions_ended.last_updated
        return auctions_ended

    def get_bazaar(self) -> Bazaar:
        """Get bazaar endpoint"""
        resp_bytes = self._http_client.get(url=_prepare_bazaar_url())
        bazaar = self._json_decoder.serialize(resp_bytes, Bazaar)
        self._bazaar_last_updated = bazaar.last_updated
        return bazaar

    @staticmethod
    def _get_continuous[T: APIEndpoint](getter: APIEndpointGetter, expected_update_interval: float) -> Iterator[T]:
        last_updated = 0
        while 1:
            next_update = last_updated / 1000 + expected_update_interval
            if next_update > time.time():  # the next update is in the future
                continue

            try:
                api_endpoint = getter()
            except Exception as e:
                logging.exception(e)
                continue

            if api_endpoint.last_updated == last_updated:
                continue  # the API has not updated yet

            last_updated = api_endpoint.last_updated
            yield api_endpoint

    def get_auctions_continuous(self) -> Iterator[Auctions]:
        return self._get_continuous(self.get_auctions, 66.5)

    def get_auctions_ended_continuous(self) -> Iterator[AuctionsEnded]:
        return self._get_continuous(self.get_auctions_ended, 66.5)

    def get_bazaar_continuous(self) -> Iterator[Bazaar]:
        return self._get_continuous(self.get_bazaar, 66.5)
