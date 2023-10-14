from typing import Any

from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException

from src.db.repositories.city_area import InjectCitiesAreaRepository
from src.db.repositories.osm_objects import InjectOSMObjectsRepository
from src.db.types.pydantic_object_id import ObjectId
from src.schemas.v1.base import CountedSchema
from src.schemas.v1.gis import GISSchema, CoordinateSchema, TagSchema

router = APIRouter(prefix="/cities")


@router.get("/{city_id}/gis")
async def get_gis_by_city(
    city_id: str,
    repo_osm: InjectOSMObjectsRepository,
    repo_city: InjectCitiesAreaRepository,
) -> CountedSchema[GISSchema]:
    try:
        city = await repo_city.find_one({"_id": ObjectId(city_id)})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid city id")
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    gis_list = await repo_osm.find({"city": city.city})

    return CountedSchema(
        count=len(gis_list),
        items=[
            GISSchema(
                id=str(gis.id),
                object_type=gis.object_type,
                coordinate=CoordinateSchema(
                    latitude=gis.coordinate.latitude,
                    longitude=gis.coordinate.longitude,
                ),
                tags=[
                    TagSchema(
                        name=tag_key,
                        value=tag_value,
                    )
                    for tag_key, tag_value in gis.tags.items()
                ],
            )
            for gis in gis_list
        ],
    )
