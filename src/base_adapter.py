import json
from abc import ABC, abstractmethod
from requests import get, Response, RequestException, HTTPError


class BaseAdapter(ABC):

    @abstractmethod
    def get_response(self) -> Response:
        pass


class Adapter(BaseAdapter):
    def __init__(self, request):
        self.request = request
        self._response: Response | None = None

    def get_response(self) -> Response:
        return get(**self.request)

    @property
    def response(self) -> Response:
        """ Геттер, если _response пустой направить запрос и записать в _response, вернуть полученный _response """
        if self._response is None:
            self._response = self.get_response()

        assert self._response is not None
        return self._response


    # def _handle_status(self, response: Response) -> Response:
    #     pass

class AdapterNominatimAPI(Adapter):

    def __init__(self, country):
        super().__init__(
            {
                "url": "https://nominatim.openstreetmap.org/search",
                "headers": {"User-Agent": "test-app/1.0"},
                "params": {"country": country,"format": "json","limit": 1}
            }
        )

    def boundingbox(self):
        return self.response

class AdapterOpenskyAPI(Adapter):

    def __init__(self, geo_data):
        super().__init__(
            {
                "url": "https://opensky-network.org/api/states/all?",
                "params": {
                    'lamin': geo_data[0],
                    'lamax': geo_data[1],
                    'lomin': geo_data[2],
                    'lomax': geo_data[3]
                }
            }
        )


api = AdapterNominatimAPI("Canada")
data_canada = api.get_response()
# print(data_canada)

response = api.boundingbox()

print(response)
# print(json.dumps(data_canada[0].get("boundingbox"), indent=4))
# api_opensky = AdapterOpenskyAPI(data_canada[0].get("boundingbox"))
# data_canada_opensky = api_opensky.get_response()
# print(json.dumps(data_canada_opensky, indent=4))