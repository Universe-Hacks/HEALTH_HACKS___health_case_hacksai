from fastapi import APIRouter

from src.depends.city import InjectCityFromPath
from src.schemas.v1.districts import DistrictWithMetric

router = APIRouter(prefix="/districts")


@router.get("/{city_id}")
async def get_city_districts(
    city: InjectCityFromPath,
) -> list[DistrictWithMetric]:
    return [
        DistrictWithMetric(
            id=str(district.id),
            name=district.name,
            polygon_coordinates=district.polygon_coordinates,
            by_type=district.density_by_type,
            by_object=district.density_by_object,
            positivity_rate=district.positivity_rate,
            negative_points_overflow=district.negative_points_overflow,
            min_negative_point_distance=district.min_negative_point_distance,
        )
        for district in city.districts
    ]
