from requests import get
from src.base_api import BaseAPI

class AdapterNominative(BaseAPI):

    def __init__(self, url: str, headers: dict, params: dict):
        super().__init__(url, headers, params)

    @classmethod
    def set_request(cls, url: str, headers: dict, params: dict):
        return cls(url, headers, params)

    def get_response( self ):
        return get(url=self.url, headers=self.headers, params=self.params)

class AdapterOpensky(BaseAPI):

    def __init__( self, url: str, headers: dict, params: dict ):
        super().__init__( url, headers, params )

    @classmethod
    def set_request( cls, url: str, headers: dict, params: dict ):
        return cls( url, headers, params )

    def get_response( self ):
        return get( url=self.url, headers=self.headers, params=self.params )


