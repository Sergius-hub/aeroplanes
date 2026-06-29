from abc import ABC, abstractmethod
from src.config import config
from psycopg2 import connect, sql

class BaseDBConnector(ABC):

    @abstractmethod
    def connect( self ):
        pass

    @abstractmethod
    def disconnect( self ):
        pass

    @abstractmethod
    def __enter__( self ):
        pass

    @abstractmethod
    def __exit__( self, exc_type, exc_val, exc_tb ):
        pass


class DBConnector(BaseDBConnector):

    def __init__( self, dbname: str ):
        self.dbname = dbname
        self._connection = None

    def connect(self):
        """Устанавливаем соединение с базой данных"""
        if self._connection is None or self._connection.closed:
            params = config()
            self._connection = connect(dbname=self.dbname, **params)
            self._connection.autocommit = True

        if self._connection is None:
            print("Ошибка соединения с базой данных")

        print("Соединение с базой данных установлено")
        return self._connection

    def disconnect(self):
        """Закрываем соединение с базой данных"""
        if self._connection is not None and not self._connection.closed:
            self._connection.close()
            self._connection = None
            print("Соединение с базой данных закрыто")

    def __enter__(self):
        """Контекстный менеджер при входе"""
        return self.connect()

    def __exit__( self, exc_type, exc_val, exc_tb ):
        """Контекстный менеджер при выходе"""
        self.disconnect()


class DBCreator:
    def __init__( self, connector: BaseDBConnector ):
        self._connector = connector

    def create_database(self, database_name: str):
        with self._connector as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}" ).format(sql.Identifier(database_name)))
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
                print("База данных создана")


    # def create_tables( self, table_name: str ):
    #     with self._connector as conn:
    #         pass



class DBManager:

    def __init__( self, connector: DBConnector ):
        self._connector = connector

    def get_countries_and_aeroplanes_count( self ):
        """Получает список всех стран и количество самолетов в их воздушных пространствах"""
        pass

    def get_all_aeroplanes( self ):
        """Получает список всех воздушных судов"""
        pass

    def get_avg_speed( self ):
        """Получает среднюю скорость по самолетам"""
        pass

    def get_aeroplanes_with_higher_speed( self ):
        """Получает список всех самолетов, у которых скорость выше средней"""
        pass

    def get_aeroplanes_with_keyword( self ):
        """Получает список всех самолетов, в позывном которых содержатся переданные в метод символы"""
        pass
