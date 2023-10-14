from fastapi import APIRouter

from src.db.repositories.city_area import InjectCitiesAreaRepository
from src.schemas.v1.base import CountedSchema
from src.schemas.v1.cities import CitySchema

router = APIRouter(prefix="/cities")


@router.get("")
async def get_all_cities(repo: InjectCitiesAreaRepository) -> CountedSchema[CitySchema]:
    cities = await repo.find()
    return CountedSchema(
        count=len(cities),
        items=[CitySchema(id=str(city.id), name=city.city) for city in cities],
    )
