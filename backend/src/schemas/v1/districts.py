from src.schemas.v1.base import BaseSchema


class MetricsByTypeSchema(BaseSchema):
    negative: float
    positive: float
    study: float


class MetricsByObjectSchema(BaseSchema):
    park: float = 0
    footway: float = 0
    pitch: float = 0
    sports_centre: float = 0
    stadium: float = 0
    track: float = 0
    market: float = 0
    greengrocer: float = 0
    farm: float = 0

    # Negative
    tobacco: float = 0
    smoke_shop: float = 0
    bar: float = 0
    pub: float = 0
    wine: float = 0
    alcohol: float = 0
    fast_food: float = 0
    food_court: float = 0

    # Studies
    university: float = 0
    college: float = 0
    school: float = 0
    kindergarten: float = 0
    language_school: float = 0
    music_school: float = 0


class CoordinatesSchema(BaseSchema):
    latitude: float
    longitude: float


class DistrictWithMetric(BaseSchema):
    name: str
    polygon_coordinates: list[CoordinatesSchema]
    by_type: MetricsByTypeSchema
    by_object: MetricsByObjectSchema
    positivity_rate: float
    negative_points_overflow: int
    min_negative_point_distance: float
