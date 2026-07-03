from typing import Self


class Aeroplane:

    def __init__(self, callsign: str, country: str, velocity: float, altitude: float):
        """Конструктор"""
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    def __str__(self) -> str:
        """Вывод строки"""
        return f"Самолет: {self.callsign} country: {self.country} volocity: {self.velocity} altitude: {self.altitude}"

    def __lt__(self, other: Self) -> bool:
        """Сравнение самолетов по высоте"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude < other.altitude

    def __gt__(self, other: Self) -> bool:
        """Сравнение самолетов по высоте"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude > other.altitude

    def __eq__(self, other: object) -> bool:
        """Сравнение самолетов по высоте"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.altitude == other.altitude

    # Геттеры и сеттеры
    @property
    def callsign(self) -> str:
        return self._callsign

    @callsign.setter
    def callsign(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Callsign должен быть строкой")
        self._callsign = value

    @property
    def country(self) -> str:
        return self._country

    @country.setter
    def country(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Country должен быть строкой")
        self._country = value

    @property
    def velocity(self) -> float:
        return self._velocity

    @velocity.setter
    def velocity(self, value: float) -> None:
        """Сеттер velocity с валидацией"""
        if not isinstance(value, (float, int)):
            print("Velocity должен быть числом")
            value = 0.0
        if value < 0:
            print("Velocity не может быть отрицательным")
            value = 0.0
        self._velocity = value

    @property
    def altitude(self) -> float:
        return self._altitude

    @altitude.setter
    def altitude(self, value: float) -> None:
        """Сеттер altitude с валидацией"""
        if not isinstance(value, (float, int)):
            print("Неправильный тип данных в 'Altitude', ожидается число")
            value = 0.0
        if not 0 <= value <= 30000:
            print(
                f"Неправильное значение 'Altitude' = {value}, у самолета '{self.callsign}' диапазон от 0 до 30000"
            )

        self._altitude = value

    @classmethod
    def read_from_raw(cls, raw_data: dict) -> list:
        """Читает данные и приводит их к типу Aeroplane"""
        return [
            cls(
                callsign=state[1].strip() if state[1] else "n/a",
                country=state[2].strip() if state[2] else "n/a",
                velocity=state[9] or 0.0,
                altitude=state[13] or 0.0,
            )
            for state in raw_data["states"]
        ]

    def to_dict(self) -> dict:
        """Возвращает словарь"""
        return {
            "callsign": self.callsign,
            "country": self.country,
            "velocity": self.velocity,
            "altitude": self.altitude,
        }
