import json
from requests import get
from src.base_aeroplanes_api import BaseAeroplanesAPI


class AeroplanesAPI(BaseAeroplanesAPI):
    def __init__(self) -> None:
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all?"
        self.aeroplanes = None

    def get_response_nominatim(self, country: str):
        # Headers с user-agent - обязательный параметр при запросе к nominatim.openstreetmap.
        # Вы можете использовать любое название вместо test-app/1.0, например просто test-app.
        headers_nominatim = {
            "User-Agent": "test-app/1.0",
        }

        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim = {
            "country": country,
            "format": 'json',
            "limit": 1,
        }

        response = get(url=self.openstreetmap_url, params=params_nominatim, headers=headers_nominatim)

        return response.json()

    def get_response_opensky(self, data: list):
        """  """
        # Пример ответа от nominatim.openstreetmap можно посмотреть в задании курсовой.
        geo_coordinates = data[0].get("boundingbox")

        # Параметры для фильтрации самолетов по их географическим координатам.
        params = {
            'lamin': geo_coordinates[0],
            'lamax': geo_coordinates[1],
            'lomin': geo_coordinates[2],
            'lomax': geo_coordinates[3],
        }

        response = get(url=self.opensky_url, params=params)

        # Пример ответа от opensky-network можно посмотреть в задании курсовой.
        return response.json()

    def get_aeroplanes(self, country: str):
        """  """
        data_country = self.get_response_nominatim(country)
        self.aeroplanes = self.get_response_opensky(data_country)


api = AeroplanesAPI()
data_nominatim = api.get_response_nominatim("Canada")
print(json.dumps(data_nominatim, indent=4))



# api = AeroplanesAPI()
# api.get_aeroplanes('Canada')