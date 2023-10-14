from src.schemas.v1.base import BaseSchema
from src.db.models.osm_objects import ObjectType


class CoordinateSchema(BaseSchema):
    latitude: float
    longitude: float


class TagSchema(BaseSchema):
    name: str
    value: str


class GISSchema(BaseSchema):
    id: str
    object_type: ObjectType
    coordinate: CoordinateSchema
    tags: list[TagSchema]
