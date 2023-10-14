from enum import StrEnum, auto

from pydantic import BaseModel as PydanticBaseModel

from src.db.models.base_model import BaseModel


class OSMCoordinate(PydanticBaseModel):
    latitude: float | None = None
    longitude: float | None = None


class OSMMember(PydanticBaseModel):
    osm_type: str
    osm_id: int


class ObjectType(StrEnum):
    POSITIVE = auto()
    NEGATIVE = auto()
    STUDY = auto()


class OSMObject(BaseModel):
    osm_id: int
    osm_type: str
    object_type: ObjectType
    coordinate: OSMCoordinate
    city: str
    district: str
    tags: dict[str, str]
    members: list[OSMMember] | None = None
    nodes: list[int] | None = None
