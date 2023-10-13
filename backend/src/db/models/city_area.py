from src.db.models.base_model import BaseModel


class CityArea(BaseModel):
    city: str
    area: float
