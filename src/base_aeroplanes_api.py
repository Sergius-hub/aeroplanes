from abc import ABC, abstractmethod

class BaseAeroplanesAPI(ABC):

    @abstractmethod
    def get_response_nominatim(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_response_opensky(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_aeroplanes(self, *args, **kwargs):
        pass

