from bson import ObjectId as BsonObjectId


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            pattern=r"^[a-f\d]{24}$",
            examples=["5e7f31f47a6ed536d130eb78", "5e7f31fcb0a9b40374bc2c91"],
            type="string",
        )

    @classmethod
    def validate(cls, v):
        return BsonObjectId(v)
