from src.db.models.base_model import BaseModel
from src.db.models.city.density import ObjectDensity, TypeDensity
from src.db.models.city.district import DistrictModel
from src.db.models.osm_objects import OSMCoordinate


class CityModel(BaseModel):
    name: str
    coordinate: OSMCoordinate
    area: float
    density_by_object: ObjectDensity
    density_by_type: TypeDensity
    districts: list[DistrictModel]

    avg_negatives_distance: float

    @property
    def positivity_metric(self) -> int:
        positive_districts = [
            district for district in self.districts if district.is_positive_rate_good
        ]
        negative_districts = [
            district for district in self.districts if not district.is_positive_rate_good
        ]
        return len(positive_districts) - len(negative_districts)

    @property
    def min_negative_point_distance(self) -> float:
        return min(district.min_negative_point_distance for district in self.districts)
