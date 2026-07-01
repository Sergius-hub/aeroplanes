from abc import ABC, abstractmethod
from src.config import config
from psycopg2 import connect, sql


class BaseDBConnector(ABC):
    """Абстракция для DBConnector"""

    def __init__(self, dbname: str = "postgres"):
        self._dbname = dbname

    def __enter__(self):
        """Контекстный менеджер при входе"""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Контекстный менеджер при выходе"""
        self.disconnect()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @property
    def dbname(self):
        return self._dbname


class DBConnector(BaseDBConnector):
    """Класс работает с подключеием и/или отключением к базе данных"""

    def __init__(self, dbname: str = "postgres", autocommit: bool = False):
        super().__init__(dbname)
        self._autocommit = autocommit
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            raise ConnectionError("Нет соединения. Вызовите connect()")
        return self._connection

    def cursor(self):
        return self.connection.cursor()

    def connect(self):
        """Устанавливаем соединение с базой данных"""
        if self._connection is None or self._connection.closed:
            params = config()
            self._connection = connect(dbname=self._dbname, **params)
            self._connection.autocommit = self._autocommit

        if self._connection is None:
            print("Ошибка соединения с базой данных")

        print("Соединение с базой данных установлено")
        return self

    def disconnect(self):
        """Закрываем соединение с базой данных"""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            self._connection = None
            print("Соединение с базой данных закрыто")


class DBCreator:
    """Класс создает базы данных по имени в коннекторе"""

    def __init__(self, connector: BaseDBConnector, database_name: str):
        self._connector = connector
        self._database_name = database_name

    def create_database(self):
        """Функция создает базу данных"""
        with self._connector as conn:
            conn.connection.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL("DROP DATABASE IF EXISTS {}").format(
                        sql.Identifier(self._database_name)
                    )
                )
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(self._database_name)
                    )
                )
                print("База данных создана")


class TBCreator:
    """Класс в базе данных создает таблицы"""

    def __init__(self, connector: BaseDBConnector):
        self._connector = connector

    def create_tables(self):
        with self._connector as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS countries (
                        country_id SERIAL PRIMARY KEY,
                        name VARCHAR(20) NOT NULL,
                        CONSTRAINT uq_countries_name UNIQUE (name)                        
                    )
                    """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS aeroplanes (
                        aeroplane_id SERIAL PRIMARY KEY,
                        country_id INTEGER NOT NULL,
                        callsign VARCHAR(10) NOT NULL,
                        velocity REAL,
                        altitude REAL,
                        CONSTRAINT fk_aeroplanes_country FOREIGN KEY (country_id) REFERENCES countries (country_id) ON DELETE RESTRICT,
                        CONSTRAINT uq_aeroplanes_callsign UNIQUE (callsign)                        
                    )
                    """)
                print("Таблицы созданы")

            conn.connection.commit()


class BaseDBManager(ABC):

    @abstractmethod
    def save_data_to_database(self, data: dict):
        pass

    @abstractmethod
    def clear_data(self):
        pass

class DBManager(BaseDBManager):

    def __init__(self, connector: BaseDBConnector):
        self._connector = connector

    def save_data_to_database(self, data: dict):
        # with self._connector as conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute("INSERT INTO countries VALUES ({})")

        for aeroplane in data:
            print(aeroplane)

    def clear_data(self):
        pass

    def get_countries_and_aeroplanes_count(self):
        """Получает список всех стран и количество самолетов в их воздушных пространствах"""
        pass

    def get_all_aeroplanes(self):
        """Получает список всех воздушных судов"""
        pass

    def get_avg_speed(self):
        """Получает среднюю скорость по самолетам"""
        pass

    def get_aeroplanes_with_higher_speed(self):
        """Получает список всех самолетов, у которых скорость выше средней"""
        pass

    def get_aeroplanes_with_keyword(self):
        """Получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        pass
