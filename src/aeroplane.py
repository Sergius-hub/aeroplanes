# from src.file_adapter import JSONFileAdapter


class Aeroplane:
    def __init__(self, callsign: str, country: str, velocity: float, altitude: float):
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.altitude = altitude

    @classmethod
    def read_from_raw(cls, raw_data):
        return [
            cls(
                callsign=state[1].strip() if state[1] else "n/a",
                country=state[2],
                velocity=state[9] or 0.0,
                altitude=state[13] or 0.0,
            )
            for state in raw_data["states"]
        ]

    @property
    def callsign(self):
        return self._callsign

    @property
    def country(self):
        return self._country

    @property
    def velocity(self):
        return self._velocity

    @property
    def altitude(self):
        return self._altitude

    @callsign.setter
    def callsign(self, value):
        if not isinstance(value, str):
            raise TypeError("Callsign должен быть строкой")
        self._callsign = value

    @country.setter
    def country(self, value):
        if not isinstance(value, str):
            raise TypeError("Country должен быть строкой")
        self._country = value

    @velocity.setter
    def velocity(self, value):
        """ Сеттер velocity с валидацией """
        if not isinstance(value, (float, int)):
            print("Velocity должен быть числом")
            value = 0.0
        if value < 0:
            print( "Velocity не может быть отрицательным" )
            value = 0.0
        self._velocity = value

    @altitude.setter
    def altitude(self, value):
        """ Сеттер altitude с валидацией """
        if not isinstance(value, (float, int)):
            print("Altitude должно быть числом")
            value = 0.0
        if not 0 <= value <= 30000:
            print( "Altitude должна быть в диапазоне от 0 до 30000" )

        self._altitude = value

    def __lt__(self, other):
        return self.altitude < other.altitude

    def __gt__(self, other):
        return self.altitude > other.altitude

    def __eq__(self, other):
        return self.altitude == other.altitude

    def to_dict(self):
        return {
            "callsign": self.callsign,
            "country": self.country,
            "velocity": self.velocity,
            "altitude": self.altitude
        }

    def __str__(self):
        return f"Самолет: {self.callsign} {self.country} {self.velocity} {self.altitude}"


