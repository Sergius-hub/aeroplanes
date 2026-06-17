from src.api_adapters import AdapterNominatimAPI, AdapterOpenskyAPI
from src.aeroplane import Aeroplane
from src.file_adapter import JSONFileAdapter
import json

def filter_aeroplanes( aeroplanes, filter_words ):
    """ Фильтрует список самолетов по странам """
    print("Фильтрация по странам:")
    return [ aeroplane for aeroplane in aeroplanes if aeroplane.country in filter_words ]

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
    aeroplanes = filter_aeroplanes( aeroplanes, country )
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

if __name__ == "__main__":

    user_interface()

