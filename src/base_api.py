from abc import ABC, abstractmethod
from requests import get


class BaseAPI(ABC):

    def __init__(self, url: str, headers: dict , params: dict ):
        self.url = url
        self.headers = headers
        self.params = params

    def get_response(self):
        return get(self.url, headers=self.headers, params=self.params)

