# aeroplanes
Собирает данные о самолетах в воздушных пространствах

## Установка

```bash
    git clone https://github.com/Sergius-hub/aeroplanes.git
```

## Описание функций

Adapter:
```Python
    class BaseAdapterAPI(ABC):
    """Абстрактный класс базового адаптера, для разных API"""

    @abstractmethod
    def get_response(self) -> Response:
        pass
    
    class HTTPAdapter(BaseAdapterAPI):
    """Класс Адаптера для получения запроса и отправки запросов"""

    def __init__(self, request: dict):
        """Конструктор"""
        ...

    def get_response(self) -> Response:
        """Метод распаковывает запрос и получает ответ"""
        ...

    @property
    def response(self) -> Response:
        """Геттер, возвращает запрос"""
        ...

    def refresh(self) -> Response:
        """Обновляем response"""
        ...

    def clear(self) -> None:
        """Сбрасывем response"""
        ...

    def _fetch(self) -> Response:
        """Выполняем запрос"""
        ...
```
Aeroplane:
```Python
class Aeroplane:

    def __init__(self, callsign: str, country: str, velocity: float, altitude: float):
        """Конструктор"""
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    # Геттеры и сеттеры
    @property
    def callsign(self) -> str:
        ...

    @callsign.setter
    def callsign(self, value: str) -> None:
        ...

    @property
    def country(self) -> str:
        ...

    @country.setter
    def country(self, value: str) -> None:
        ...

    @property
    def velocity(self) -> float:
        ...

    @velocity.setter
    def velocity(self, value: float) -> None:
        """Сеттер velocity с валидацией"""
        ...

    @property
    def altitude(self) -> float:
        ...

    @altitude.setter
    def altitude(self, value: float) -> None:
        """Сеттер altitude с валидацией"""
        ...

    @classmethod
    def read_from_raw(cls, raw_data: dict) -> list:
        """Читает данные и приводит их к типу Aeroplane"""
        ...

    def __lt__(self, other: Aeroplane) -> bool:
        """Сравнение самолетов по высоте"""
        ...

    def __gt__(self, other: Aeroplane) -> bool:
        """Сравнение самолетов по высоте"""
        ...

    def __eq__(self, other: object) -> bool:
        """Сравнение самолетов по высоте"""
        ...

    def to_dict(self) -> dict:
        """Возвращает словарь"""
        ...

    def __str__(self) -> str:
        """Вывод строки"""
        ...
```
FileAdapter:
```Python
class BaseFileAdapter(ABC):

    @abstractmethod
    def save(self, *args):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class JSONFileAdapter(BaseFileAdapter):
    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename

    def save(self, *args):
		"""Сохраняет информацию в файл"""
        ...

    def load(self):
        """Загружает информацию из файла"""
		...

    def delete(self):
        pass
```

## Тестирование
Тесты конструктора и свойств
```commandline
    def test_init_valid_data(self):
        """Тест корректной инициализации"""
    ...
```
Тесты геттеров и сеттеров
```commandline
    def test_callsign_setter_valid(self):
        """Тест установки корректного callsign"""
    def test_callsign_setter_invalid_type(self):
        """Тест: callsign не строка -> TypeError"""
    ...
```
Тесты методов сравнения
```    
    def test_lt(self):
        """Тест оператора <"""
    def test_gt(self):
        """Тест оператора >"""
    def test_eq(self):
        """Тест оператора =="""
    def test_compare_with_non_aeroplane(self):
        """Тест сравнения с объектом другого типа"""
```
Тесты метода read_from_raw:
```commandline
    def test_read_from_raw_valid_data(self):
        """Тест чтения из корректных сырых данных"""
```

Тесты для HTTPAdapter:
```commandline
    def test_init_valid_request(self):
        """Создание адаптера с валидным запросом"""
    def test_init_request_none(self):
        """Создание адаптера с None -> ошибка"""
    def test_fetch_direct_call(self):
        """Прямой вызов _fetch для проверки логики"""
    ...
```

