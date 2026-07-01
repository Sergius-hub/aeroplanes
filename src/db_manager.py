from abc import ABC, abstractmethod
from src.config import config
from psycopg2 import connect, sql
from typing import Any

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
                        CONSTRAINT fk_aeroplanes_country FOREIGN KEY (country_id) REFERENCES countries (country_id) ON DELETE RESTRICT                                              
                    )
                    """)
                print("Таблицы созданы")

            conn.connection.commit()


class BaseDBManager(ABC):

    def __init__(self, db_name: str = "aeroplanes_db"):
        self.db_name = db_name


    @abstractmethod
    def save_data_to_database(self, data: list[dict[str, Any]]):
        pass

    @abstractmethod
    def clear_data(self):
        pass

    def setup_db(self):
        """Метод создает базу данных и таблицы"""
        # Создаем базу данных
        connector_postgres = DBConnector()
        creator_db = DBCreator( connector_postgres, self.db_name )
        creator_db.create_database()

        # Создаем таблицы
        connector_db = DBConnector( self.db_name )
        creator_tb = TBCreator( connector_db )
        creator_tb.create_tables()


class DBManager(BaseDBManager):
    """Класс, который может соединяться с базой данных, записывать в базу и получать информацию"""

    def __init__(self, db_name: str = "aeroplanes_db"):
        super().__init__(db_name)

    def save_data_to_database(self, data: list[dict[str, Any]]):
        """Метод сохраняет информацию из словаря в базу данных"""
        with DBConnector( self.db_name ) as conn:
            with conn.cursor() as cursor:
                for aeroplane in data:
                    cursor.execute(
                        """
                        INSERT INTO countries (name) VALUES (%s)
                        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
                        RETURNING country_id
                        """,
                        (aeroplane["country"],)
                    )
                    country_id = cursor.fetchone()[0]

                    cursor.execute(
                        """
                        INSERT INTO aeroplanes (country_id, callsign, velocity, altitude)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (country_id, aeroplane["callsign"], aeroplane["velocity"], aeroplane["altitude"])
                    )
            conn.connection.commit()
        print(f"Информация в базу данных {self.db_name} добавлена")

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
