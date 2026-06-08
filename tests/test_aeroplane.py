import pytest
from src.aeroplane import Aeroplane


class TestAeroplaneInit:
    """Тесты конструктора и свойств"""

    def test_init_valid_data(self):
        """Тест корректной инициализации"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)

        assert plane.callsign == "ABC123"
        assert plane.country == "USA"
        assert plane.velocity == 850.5
        assert plane.altitude == 10000

    def test_init_with_integer_velocity(self):
        """Тест: скорость передана как int (должна стать float)"""
        plane = Aeroplane("ABC123", "USA", 850, 10000)
        assert plane.velocity == 850.0

    def test_init_with_integer_altitude(self):
        """Тест: высота передана как int (должна стать float)"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        assert plane.altitude == 10000.0


class TestAeroplaneProperties:
    """Тесты геттеров и сеттеров"""

    def test_callsign_setter_valid(self):
        """Тест установки корректного callsign"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.callsign = "XYZ789"
        assert plane.callsign == "XYZ789"

    def test_callsign_setter_invalid_type(self):
        """Тест: callsign не строка -> TypeError"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        with pytest.raises(TypeError, match="Callsign должен быть строкой"):
            plane.callsign = 123  # type: ignore

    def test_country_setter_valid(self):
        """Тест установки корректного country"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.country = "Russia"
        assert plane.country == "Russia"

    def test_country_setter_invalid_type(self):
        """Тест: country не строка -> TypeError"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        with pytest.raises(TypeError, match="Country должен быть строкой"):
            plane.country = 123  # type: ignore

    def test_velocity_setter_valid(self):
        """Тест установки корректной скорости"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.velocity = 900.0
        assert plane.velocity == 900.0

    def test_velocity_setter_negative(self, capsys):
        """Тест: отрицательная скорость -> печатает предупреждение, устанавливает 0.0"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.velocity = -100.0
        captured = capsys.readouterr()
        assert "Velocity не может быть отрицательным" in captured.out
        assert plane.velocity == 0.0

    def test_velocity_setter_not_number(self, capsys):
        """Тест: скорость не число -> печатает предупреждение, устанавливает 0.0"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.velocity = "abc"  # type: ignore
        captured = capsys.readouterr()
        assert "Velocity должен быть числом" in captured.out
        assert plane.velocity == 0.0

    def test_altitude_setter_valid(self):
        """Тест установки корректной высоты"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.altitude = 15000.0
        assert plane.altitude == 15000.0

    def test_altitude_setter_below_range(self, capsys):
        """Тест: высота ниже 0 -> печатает предупреждение, но все равно устанавливает"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.altitude = -500.0
        captured = capsys.readouterr()
        assert "Altitude должна быть в диапазоне от 0 до 30000" in captured.out
        # Сеттер не сбрасывает значение, только печатает предупреждение
        assert plane.altitude == -500.0

    def test_altitude_setter_above_range(self, capsys):
        """Тест: высота выше 30000 -> печатает предупреждение"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.altitude = 35000.0
        captured = capsys.readouterr()
        assert "Altitude должна быть в диапазоне от 0 до 30000" in captured.out

    def test_altitude_setter_not_number(self, capsys):
        """Тест: высота не число -> печатает предупреждение, устанавливает 0.0"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        plane.altitude = "abc"  # type: ignore
        captured = capsys.readouterr()
        assert "Altitude должно быть числом" in captured.out
        assert plane.altitude == 0.0


class TestAeroplaneComparisons:
    """Тесты методов сравнения"""

    def test_lt(self):
        """Тест оператора <"""
        plane1 = Aeroplane("A1", "USA", 500, 10000)
        plane2 = Aeroplane("A2", "USA", 500, 20000)
        assert plane1 < plane2
        assert not (plane2 < plane1)

    def test_gt(self):
        """Тест оператора >"""
        plane1 = Aeroplane("A1", "USA", 500, 10000)
        plane2 = Aeroplane("A2", "USA", 500, 20000)
        assert plane2 > plane1
        assert not (plane1 > plane2)

    def test_eq(self):
        """Тест оператора =="""
        plane1 = Aeroplane("A1", "USA", 500, 10000)
        plane2 = Aeroplane("A2", "USA", 500, 10000)
        plane3 = Aeroplane("A3", "USA", 500, 20000)
        assert plane1 == plane2
        assert plane1 != plane3

    def test_compare_with_non_aeroplane(self):
        """Тест сравнения с объектом другого типа"""
        plane = Aeroplane("A1", "USA", 500, 10000)
        assert plane != 123
        assert plane != "string"
        assert plane != None  # noqa: E711


class TestAeroplaneReadFromRaw:
    """Тесты метода read_from_raw"""

    def test_read_from_raw_valid_data(self):
        """Тест чтения из корректных сырых данных"""
        raw_data = {
            "states": [
                [
                    1,
                    "ABC123",
                    "USA",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    500.0,
                    None,
                    None,
                    None,
                    10000.0,
                ],
                [
                    2,
                    "XYZ789",
                    "Russia",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    600.0,
                    None,
                    None,
                    None,
                    20000.0,
                ],
            ]
        }
        planes = Aeroplane.read_from_raw(raw_data)

        assert len(planes) == 2
        assert planes[0].callsign == "ABC123"
        assert planes[0].country == "USA"
        assert planes[0].velocity == 500.0
        assert planes[0].altitude == 10000.0

        assert planes[1].callsign == "XYZ789"
        assert planes[1].country == "Russia"
        assert planes[1].velocity == 600.0
        assert planes[1].altitude == 20000.0

    def test_read_from_raw_empty_states(self):
        """Тест: пустой список states"""
        raw_data = {"states": []}
        planes = Aeroplane.read_from_raw(raw_data)
        assert planes == []

    def test_read_from_raw_missing_callsign(self):
        """Тест: отсутствует callsign -> значение 'n/a'"""
        raw_data = {
            "states": [
                [
                    1,
                    None,
                    "USA",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    500.0,
                    None,
                    None,
                    None,
                    10000.0,
                ]
            ]
        }
        planes = Aeroplane.read_from_raw(raw_data)
        assert planes[0].callsign == "n/a"

    def test_read_from_raw_missing_velocity(self):
        """Тест: отсутствует velocity -> 0.0"""
        raw_data = {
            "states": [
                [
                    1,
                    "ABC123",
                    "USA",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    10000.0,
                ]
            ]
        }
        planes = Aeroplane.read_from_raw(raw_data)
        assert planes[0].velocity == 0.0

    def test_read_from_raw_missing_altitude(self):
        """Тест: отсутствует altitude -> 0.0"""
        raw_data = {
            "states": [
                [
                    1,
                    "ABC123",
                    "USA",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    500.0,
                    None,
                    None,
                    None,
                    None,
                ]
            ]
        }
        planes = Aeroplane.read_from_raw(raw_data)
        assert planes[0].altitude == 0.0


class TestAeroplaneToDict:
    """Тесты метода to_dict"""

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        result = plane.to_dict()

        expected = {
            "callsign": "ABC123",
            "country": "USA",
            "velocity": 850.5,
            "altitude": 10000,
        }
        assert result == expected


class TestAeroplaneStr:
    """Тесты метода __str__"""

    def test_str(self):
        """Тест строкового представления"""
        plane = Aeroplane("ABC123", "USA", 850.5, 10000)
        result = str(plane)
        assert "Самолет:" in result
        assert "ABC123" in result
        assert "USA" in result
        assert "850.5" in result
        assert "10000" in result
