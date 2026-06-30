from abc import ABC, abstractmethod
from src.config import config
from psycopg2 import connect, sql

class BaseDBConnector(ABC):
    """Абстракция для DBConnector"""

    def __init__( self, dbname: str="postgres" ):
        self._dbname = dbname

    @property
    def dbname( self ):
        return self._dbname

    @abstractmethod
    def connect( self ):
        pass

    @abstractmethod
    def disconnect( self ):
        pass

    def __enter__( self ):
        """Контекстный менеджер при входе"""
        return self.connect()

    def __exit__( self, exc_type, exc_val, exc_tb ):
        """Контекстный менеджер при выходе"""
        self.disconnect()


class DBConnector(BaseDBConnector):
    """Класс работает с подключеием и/или отключением к базе данных"""
    def __init__(self, dbname: str="postgres", autocommit: bool=False):
        super().__init__(dbname)
        self._autocommit = autocommit
        self._connection = None

    @property
    def connection( self ):
        if self._connection is None:
            raise ConnectionError( "Нет соединения. Вызовите connect()" )
        return self._connection

    def cursor( self ):
        return self._connection.cursor()

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
    """Класс работает с созданием базы данных и таблиц внутри нее"""
    def __init__(self, connector: BaseDBConnector):
        self._connector = connector

    def create_database(self):

        conn = self._connector.connect()
        conn.connection.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}" ).format(sql.Identifier(self._connector.dbname)))
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(self._connector.dbname)))
            print("База данных создана")

        conn.disconnect()



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
