from src.schemas.v1.base import BaseSchema
from src.schemas.v1.gis import CoordinateSchema


class CitySchema(BaseSchema):
    id: str
    name: str
    coordinate: CoordinateSchema
