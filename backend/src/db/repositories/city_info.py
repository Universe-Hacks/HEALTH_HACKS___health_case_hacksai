from typing import Annotated, TypeAlias

from fastapi import Depends

from src.db.models.city_info import CityInfo
from src.db.repositories.base_repository import BaseRepository


class CityInfoRepository(BaseRepository):
    model = CityInfo
    database_name = "osm"
    collection_name = "city_info"


InjectCitiesInfoRepository: TypeAlias = Annotated[CityInfoRepository, Depends()]
