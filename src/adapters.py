from requests import get
from src.base_api import BaseAPI


class Adapter(BaseAPI):
    def __init__( self, url: str, headers: dict, params: dict ):
        super().__init__(url, headers, params)

    def get_response( self ):
        return get(url=self.url, headers=self.headers, params=self.params)

class AdapterNominative(Adapter):

    def __init__( self, country: str):
        super().__init__(
            url="https://nominatim.openstreetmap.org/search",
            headers={
                "User-Agent": "test-app/1.0"
            },
            params={
                "country": country,
                "format": 'json',
                "limit": 1,
            }
        )


class AdapterOpensky(Adapter):

    def __init__( self, data: list):

        geo_coordinates = data[0].get( "boundingbox" )
        params = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }

        super().__init__(
            url="https://opensky-network.org/api/states/all?",
            params=params
        )

