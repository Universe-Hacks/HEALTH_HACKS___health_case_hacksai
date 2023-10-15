from fastapi import APIRouter

from src.depends.city import InjectCityFromPath
from src.schemas.v1.recs import RecsSchema

router = APIRouter(prefix="/cities")


@router.get("/{city_id}/recs")
async def get_metrics_by_city(city: InjectCityFromPath) -> list[RecsSchema]:
    recs = []
    if city.min_negative_point_distance < 100:
        recs.append(
            RecsSchema(
                key="Минимальное расстояние до учебных учреждений",
                value="Необходимо убрать отрицательные объекты от учебных учреждений",
            )
        )

    if city.avg_negatives_distance < 200:
        recs.append(
            RecsSchema(
                key="Средняя плотность отрицательных объектов",
                value="Необходимо снизить плотность негативных объектов",
            )
        )
    return recs
