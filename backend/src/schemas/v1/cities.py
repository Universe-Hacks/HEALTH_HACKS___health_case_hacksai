from src.db.models.base_model import BaseModel


class CitySchema(BaseModel):
    id: str
    name: str
