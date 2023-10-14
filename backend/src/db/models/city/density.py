from src.db.models.base_model import BaseModel


class ObjectDensity(BaseModel):
    # Positive
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


class TypeDensity(BaseModel):
    positive: float = 0
    negative: float = 0
    study: float = 0
