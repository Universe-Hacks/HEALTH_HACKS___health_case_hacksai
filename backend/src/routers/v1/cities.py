from fastapi import APIRouter

from src.db.models.city_info import CityInfo
from src.db.repositories.city_info import InjectCitiesInfoRepository
from src.schemas.v1.base import CountedSchema
from src.schemas.v1.cities import CitySchema

router = APIRouter(prefix="/cities")


@router.get("")
async def get_all_cities(repo: InjectCitiesInfoRepository) -> CountedSchema[CitySchema]:
    cities: list[CityInfo] = await repo.find()
    return CountedSchema(
        count=len(cities),
        items=[
            CitySchema(
                id=str(city.id),
                name=city.city,
                positive_density=city.density_by_type.positive,
                negative_density=city.density_by_type.negative,
                study_density=city.density_by_type.study,
            )
            for city in cities
        ],
    )
