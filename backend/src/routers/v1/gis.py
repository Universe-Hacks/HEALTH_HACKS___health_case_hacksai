from fastapi import APIRouter

from src.db.repositories.osm_objects import InjectOSMObjectsRepository
from src.depends.city import InjectCityFromPath, InjectDistrictFromPath
from src.schemas.v1.base import CountedSchema
from src.schemas.v1.gis import CoordinateSchema, GISSchema, TagSchema

router = APIRouter(prefix="/cities")


@router.get("/{city_id}/gis")
async def get_gis_by_city(
    city: InjectCityFromPath,
    repo_osm: InjectOSMObjectsRepository,
) -> CountedSchema[GISSchema]:
    gis_list = await repo_osm.find({"city": city.name})
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


@router.get("/{city_id}/{district_id}/gis")
async def get_gis_by_district(
    city: InjectCityFromPath,
    district: InjectDistrictFromPath,
    repo_osm: InjectOSMObjectsRepository,
) -> CountedSchema[GISSchema]:
    gis_list = await repo_osm.find({"city": city.name, "district": district.name})
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
