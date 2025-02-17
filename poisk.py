from io import BytesIO
from math import sqrt

import sys
import requests
from PIL import Image

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

address_ll = ','.join(toponym["Point"]["pos"].split(' '))

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "results": 10,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass

# Преобразуем ответ в json-объект
json_response = response.json()

organizations = json_response["features"][:11]
# Название организации.


def map_params(toponym):
    # Координаты центра топонима:
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
    pt = f'{toponym_longitude},{toponym_lattitude},pm2rdl'

    # Собираем параметры для запроса к StaticMapsAPI:
    for organization in organizations:
        time = organization['properties']['CompanyMetaData']['Hours']['text']
        point = organization["geometry"]["coordinates"]
        org_point = f"{point[0]},{point[1]}"
        if 'круглосуточно' in time:
            pt += f'~{org_point},pm2dgl'
        elif time == '':
            pt += f'~{org_point},pm2grl'
        else:
            pt += f'~{org_point},pm2dbl'
    map_params = {
        "apikey": apikey,
        "pt": pt

    }
    return map_params


toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params(toponym))
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
