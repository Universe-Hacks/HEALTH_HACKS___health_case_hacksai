from backend.src.db.models.city_area import CityArea
from backend.src.db.repositories.base_repository import BaseRepository


class CityAreaRepository(BaseRepository[CityArea]):
    model = CityArea
    database_name = "osm"
    collection_name = "city_area"
