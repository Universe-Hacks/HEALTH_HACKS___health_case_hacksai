from src.db.models.base_model import BaseModel
from src.db.models.city.density import ObjectDensity, TypeDensity


class DistrictModel(BaseModel):
    name: str
    area: float
    density_by_object: ObjectDensity
    density_by_type: TypeDensity

    positivity_rate: float

    negative_points_overflow: int

    min_negative_point_distance: float

    @property
    def is_positive_rate_good(self) -> bool:
        return self.positivity_rate > 1.5
