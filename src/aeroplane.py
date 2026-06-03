from src.adapter_api import AdapterAPI

class Aeroplane(AdapterAPI):
    def __init__(self, country):
        super().__init__(country)



aeroplane = Aeroplane("Canada")

