import math

from src.misc.gis.dto import CoordinateDTO


def calculate_distance_in_meters(
    first_coordinate: CoordinateDTO,
    second_coordinate: CoordinateDTO,
) -> float:
    # Преобразование градусов в радианы
    lat1 = math.radians(first_coordinate.latitude)
    lon1 = math.radians(first_coordinate.longitude)
    lat2 = math.radians(second_coordinate.latitude)
    lon2 = math.radians(second_coordinate.longitude)

    # Разница широты и долготы
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Вычисление расстояния
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c * 1000  # расстояние в метрах
    return distance
