from aeroplane import Aeroplane
from db_manager import DBConnector, TBCreator
from src.api_adapters import AdapterNominatimAPI, AdapterOpenskyAPI
from src.aeroplane import Aeroplane
from src.file_adapter import JSONFileAdapter
from src.db_manager import DBCreator, DBConnector, DBManager
import json


def filter_aeroplanes_by_countries( aeroplanes, filter_words ):
    """ Фильтрует список самолетов по странам """
    print(f"Фильтрация по странам {filter_words}:")
    return [ aeroplane for aeroplane in aeroplanes if aeroplane.country in filter_words ]

def filter_aeroplanes_by_altitude_and_velocity( aeroplanes, altitude: float=0.0, velocity: float=0.0 ):
    """ Фильтрует список самолетов по странам """
    return [ aeroplane for aeroplane in aeroplanes if aeroplane.altitude <= altitude and aeroplane.velocity >= velocity ]

def get_aeroplanes_by_altitude( aeroplanes, altitude_range ):
    """ Фильтрует список самолетов по диапазону высоты """
    lower_altitude, upper_altitude = (int(part.strip()) for part in altitude_range.split( "-" ))
    print(f"Диапазон {altitude_range}:")
    return [aeroplane for aeroplane in aeroplanes if lower_altitude <= aeroplane.altitude <= upper_altitude]

def sort_aeroplanes( aeroplanes, reverse:bool=True ):
    """ Сортировка списка самолетов """
    print("Сортировка самолетов:")
    return sorted(aeroplanes, reverse=reverse)

def get_top_aeroplanes( aeroplanes, top_n ):
    """ Формирует топ n самолетов сверху списка """
    print(f"Топ {top_n} самолетов:")
    return aeroplanes[0:top_n]

def print_aeroplanes( aeroplanes ):
    """ Печать списка самолетов """
    for aeroplane in aeroplanes:
        print( aeroplane )

def get_aeroplanes_from_countries( countries: list ):
    for country in countries:
        api_nominatim = AdapterNominatimAPI( country )
        bbox = api_nominatim.boundingbox()
        api_opensky = AdapterOpenskyAPI( bbox )
        raw_data = api_opensky.response.json()

        aeroplanes = Aeroplane.read_from_raw( raw_data )
        aeroplanes = filter_aeroplanes_by_countries( aeroplanes, country )
        aeroplanes = filter_aeroplanes_by_altitude_and_velocity( aeroplanes, 30000.0, 10.0)
        print_aeroplanes(aeroplanes)

def user_interface():
    country = input( "Введите название страны: " )
    # top_n = int( input( "Введите количество самолетов для вывода в топ N: " ) )
    # filter_words = input( "Введите названия стран для фильтрации по стране регистрации: " ).split()
    # altitude_range = input( "Введите диапазон высот полета: " )  # Пример: 100000 - 150000


    api_nominatim = AdapterNominatimAPI( country )
    bbox = api_nominatim.boundingbox()
    api_opensky = AdapterOpenskyAPI( bbox )
    raw_data = api_opensky.response.json()

    aeroplanes = Aeroplane.read_from_raw(raw_data)
    aeroplanes = filter_aeroplanes_by_countries( aeroplanes, country )
    print_aeroplanes(aeroplanes)

    # sorted_aeroplanes = sort_aeroplanes(aeroplanes)
    # print_aeroplanes( sorted_aeroplanes )
    #
    # top_n_a = get_top_aeroplanes(aeroplanes, 2)
    # print_aeroplanes(top_n_a)
    #
    # ranged_aeroplanes = get_aeroplanes_by_altitude(aeroplanes, "1000 - 2500")
    # print_aeroplanes(ranged_aeroplanes)
    #
    # print_aeroplanes(filter_aeroplanes( aeroplanes, country ))

    json_file = JSONFileAdapter(f"{country}_aeroplanes.json")
    json_file.save( *aeroplanes )

    # data = json_file.load()
    # print(data)
    # print(type(data))

def db_create():

    db_name = "aeroplanes_db"

    # Создаем базы данных
    connector_postgres = DBConnector()
    creator_db = DBCreator(connector_postgres, db_name)
    creator_db.create_database()

    # Создаем таблицы
    connector_db = DBConnector( db_name )
    creator_tb = TBCreator(connector_db)
    creator_tb.create_tables()

def save_db():
    get_aeroplanes_from_countries(["Spain", "Italy", "Japan", "France"])
    # db = DBManager()

if __name__ == "__main__":

    # user_interface()
    # db_create()
    save_db()