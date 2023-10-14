from typing import Annotated, TypeAlias

from bson.errors import InvalidId
from fastapi import Depends, HTTPException, Path

from src.db.models.city.city_model import CityModel
from src.db.models.city.district import DistrictModel
from src.db.repositories.city import InjectCityRepository
from src.db.types.pydantic_object_id import ObjectId


async def get_city_from_path(
    city_id: Annotated[str, Path()],
    repo_city: InjectCityRepository,
) -> CityModel:
    try:
        city: CityModel | None = await repo_city.find_one({"_id": ObjectId(city_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid city id")
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


async def get_district_from_path(
    district_id: Annotated[str, Path()],
    repo_city: InjectCityRepository,
) -> DistrictModel:
    try:
        city: CityModel | None = await repo_city.find_one(
            {"districts._id": ObjectId(district_id)}
        )
        district = next(filter(lambda d: str(d.id) == district_id, city.districts))
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid city id")
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return district


InjectCityFromPath: TypeAlias = Annotated[CityModel, Depends(get_city_from_path)]
InjectDistrictFromPath: TypeAlias = Annotated[
    DistrictModel, Depends(get_district_from_path)
]
