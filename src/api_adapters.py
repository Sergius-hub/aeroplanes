from src.api_adapter import HTTPAdapter


class AdapterNominatimAPI(HTTPAdapter):

    def __init__(self, country: str = "Canada"):
        super().__init__(
            {
                "url": "https://nominatim.openstreetmap.org/search",
                "headers": {"User-Agent": "test-app/1.0"},
                "params": {"country": country, "format": "json", "limit": 1},
            }
        )

    def boundingbox(self):
        return self.response.json()[0]["boundingbox"]


class AdapterOpenskyAPI(HTTPAdapter):

    def __init__(self, geo_data):
        super().__init__(
            {
                "url": "https://opensky-network.org/api/states/all?",
                "params": {
                    "lamin": geo_data[0],
                    "lamax": geo_data[1],
                    "lomin": geo_data[2],
                    "lomax": geo_data[3],
                },
            }
        )
