from abc import ABC, abstractmethod
from requests import get, Response


class BaseAdapterAPI(ABC):
    """ Абстрактный класс базового адаптера, для разных API """
    @abstractmethod
    def get_response(self) -> Response:
        pass


class HTTPAdapter(BaseAdapterAPI):
    """ Класс Адаптера для получения запроса и отправки запросов """
    def __init__(self, request):
        """ Конструктор """
        if request is None:
            raise ValueError("request не может быть None")

        self._request = request
        self._response: Response | None = None


    def get_response(self) -> Response:
        """ Метод распаковывает запрос и получает ответ """

        if self._response is None:
            self._response = self._fetch()

        assert self._response is not None
        return self._response


    @property
    def response(self) -> Response:
        """ Геттер, возвращает запрос """
        return self.get_response()

    def refresh( self ) -> Response:
        """ Обновляем response """
        self.clear()
        return self.get_response()

    def clear(self) -> None:
        """ Сбрасывем response """
        self._response = None

    def _fetch( self ) -> Response:
        """ Выполняем запрос """
        response_ = get( **self._request )
        response_.raise_for_status()
        return response_
