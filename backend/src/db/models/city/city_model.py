from src.db.models.base_model import BaseModel
from src.db.models.city.density import ObjectDensity, TypeDensity


class CityModel(BaseModel):
    name: str
    area: float
    density_by_object: ObjectDensity
    density_by_type: TypeDensity
