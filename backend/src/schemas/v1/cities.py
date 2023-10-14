from src.schemas.v1.base import BaseSchema


class CitySchema(BaseSchema):
    id: str
    name: str
    positive_density: float
    negative_density: float
    study_density: float

    positivity_metric: int
