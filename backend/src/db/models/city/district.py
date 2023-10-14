from src.db.models.base_model import BaseModel
from src.db.models.city.density import ObjectDensity, TypeDensity
from src.db.models.osm_objects import OSMCoordinate


class DistrictModel(BaseModel):
    name: str
    area: float
    density_by_object: ObjectDensity
    density_by_type: TypeDensity

    polygon_coordinates: list[OSMCoordinate]

    positivity_rate: float
    negative_points_overflow: int
    min_negative_point_distance: float

    @property
    def is_positive_rate_good(self) -> bool:
        return self.positivity_rate > 1.5
