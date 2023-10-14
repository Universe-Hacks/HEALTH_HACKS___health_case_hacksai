from fastapi import APIRouter

from src.db.models.city.city_model import CityModel
from src.db.repositories.city import InjectCityRepository
from src.schemas.v1.base import CountedSchema
from src.schemas.v1.cities import CitySchema

router = APIRouter(prefix="/cities")


@router.get("")
async def get_all_cities(repo: InjectCityRepository) -> CountedSchema[CitySchema]:
    cities: list[CityModel] = await repo.find()
    return CountedSchema(
        count=len(cities),
        items=[
            CitySchema(
                id=str(city.id),
                name=city.name,
                coordinate=city.coordinate,
            )
            for city in cities
        ],
    )
