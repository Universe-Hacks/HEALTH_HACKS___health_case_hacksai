from fastapi import APIRouter

from src.depends.city import InjectCityFromPath
from src.schemas.v1.metrics import (
    MetricSchema,
    MetricsByTypeSchema,
    MetricsByObjectSchema,
)

router = APIRouter(prefix="/cities")


@router.get("/{city_id}/metrics")
async def get_metrics_by_city(city: InjectCityFromPath) -> MetricSchema:
    return MetricSchema(
        by_type=MetricsByTypeSchema(**city.density_by_type.model_dump()),
        by_object=MetricsByObjectSchema(**city.density_by_object.model_dump()),
    )
