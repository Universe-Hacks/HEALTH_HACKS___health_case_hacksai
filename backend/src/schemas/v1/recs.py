from src.schemas.v1.base import BaseSchema


class RecsSchema(BaseSchema):
    key: str
    value: str
