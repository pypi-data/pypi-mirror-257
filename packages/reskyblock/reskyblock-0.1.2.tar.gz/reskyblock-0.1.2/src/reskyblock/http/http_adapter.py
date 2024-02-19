"""This module provides all needed functionality for dealing with http requests"""
from abc import ABC, abstractmethod

import httpx

__all__ = (
    "AbstractHTTPClient",
    "HTTPXClient",
)


class AbstractHTTPClient(ABC):
    """Abstract interface for an HTTP client"""

    @abstractmethod
    def get(self, url: str, params: dict | None = None) -> bytes:
        """Sends a GET HTTP request to a URL
        :param url: URL to be fetched
        :param params: parameters to be added to the request
        :return: response as bytes
        """


class HTTPXClient(AbstractHTTPClient):
    def __init__(self) -> None:
        self._session: httpx.Client = httpx.Client()

    def get(self, url: str, params: dict | None = None) -> bytes:
        """Sends a GET HTTP request to a URL. If an exception is thrown,
        retries sending the same request after `retry_time` seconds.
        :param url: URL to be fetched
        :param params: parameters to be added to the request
        :return: response as bytes
        """

        return self._session.get(url, params=params).raise_for_status().content
