from bson import ObjectId
from pydantic import BaseConfig, Field
from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")

    def __init__(self, **kwargs):
        """
        Excludes None values before validation.
        This allows to use default value if None is provided.
        """
        super().__init__(**{k: v for k, v in kwargs.items() if v is not None})

    class Config(BaseConfig):
        validate_assignment = True
        populate_by_name = True
        json_encoders = {
            ObjectId: str,
        }
        arbitrary_types_allowed = True
