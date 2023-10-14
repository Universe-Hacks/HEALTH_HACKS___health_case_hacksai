from typing import Annotated, TypeAlias

from fastapi import Depends

from src.db.models.city.city_model import CityModel
from src.db.repositories.base_repository import BaseRepository


class CityRepository(BaseRepository):
    model = CityModel
    database_name = "osm"
    collection_name = "cities"


InjectCityRepository: TypeAlias = Annotated[CityRepository, Depends()]
