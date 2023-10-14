from src.db.models.base_model import BaseModel


class CitySchema(BaseModel):
    id: str
    name: str
    positive_density: float
    negative_density: float
    study_density: float
