def map_params(toponym):
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    left_corner = toponym['boundedBy']['Envelope']['upperCorner']
    right_corner = toponym['boundedBy']['Envelope']['lowerCorner']
    delta = str(min(float(left_corner.split(' ')[0]) - float(right_corner.split(' ')[0]),
                    float(left_corner.split(' ')[1]) - float(right_corner.split(' ')[1])))
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "apikey": apikey,
        "pt": f'{toponym_longitude},{toponym_lattitude},comma'

    }
    return map_params
