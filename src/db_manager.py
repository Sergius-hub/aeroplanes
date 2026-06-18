from abc import ABC, abstractmethod


class BaseDBConnector(ABC):

    @abstractmethod
    def connect( self ):
        pass


class DBConnector(BaseDBConnector):
    pass


class BaseDBManager(ABC):
    pass



class DBManager(BaseDBManager):

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
