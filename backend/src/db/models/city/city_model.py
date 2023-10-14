from src.db.models.base_model import BaseModel
from src.db.models.city.density import ObjectDensity, TypeDensity
from src.db.models.city.district import DistrictModel


class CityModel(BaseModel):
    name: str
    area: float
    density_by_object: ObjectDensity
    density_by_type: TypeDensity
    districts: list[DistrictModel]
