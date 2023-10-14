from typing import Annotated, TypeAlias

from bson.errors import InvalidId
from fastapi import Depends, HTTPException, Path

from src.db.models.city.city_model import CityModel
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


InjectCityFromPath: TypeAlias = Annotated[CityModel, Depends(get_city_from_path)]
