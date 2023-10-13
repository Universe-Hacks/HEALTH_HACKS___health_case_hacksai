from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, Union

from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertManyResult, InsertOneResult, UpdateResult

from backend.settings import settings
from backend.src.db.models.base_model import BaseModel
from backend.src.db.types.pydantic_object_id import ObjectId

T = TypeVar("T", bound=BaseModel)

Filter = Union[dict[str, dict | float | int | list | str], ObjectId]


class BaseRepository(ABC, Generic[T]):
    @property
    @abstractmethod
    def model(self) -> type[T]:
        raise NotImplementedError

    database_name: str
    collection_name: str

    client: AgnosticClient
    database: AgnosticDatabase
    collection: AgnosticCollection

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.database = self.client[self.database_name]
        self.collection = self.database[self.collection_name]

    async def find(self, _filter: Filter | None = None) -> list[T]:
        docs = []
        async for doc in self.collection.find(filter=_filter):
            docs.append(self.model(**doc))
        return docs

    async def find_one(self, _filter: Filter | None = None) -> T | None:
        doc: dict[str, Any] | None = await self.collection.find_one(filter=_filter)
        if doc is not None:
            return self.model(**doc)

    async def insert_many(self, docs: list[T]) -> InsertManyResult:
        return await self.collection.insert_many(
            documents=[doc.model_dump(by_alias=True, exclude_none=True) for doc in docs], ordered=False,
        )

    async def insert_one(self, doc: T) -> InsertOneResult:
        return await self.collection.insert_one(document=doc.model_dump(by_alias=True, exclude_none=True))

    async def update_one(self, doc: T, upsert=False) -> UpdateResult:
        update: dict[str, dict] = {
            "$set": doc.model_dump(exclude={"_id"}, by_alias=True, exclude_none=True),
            "$unset": {k: True for k, v in doc.model_dump(exclude={"_id"}, by_alias=True).items() if v is None},
        }
        update: dict[str, dict] = {k: v for k, v in update.items() if v}
        return await self.collection.update_one(filter={"_id": doc.id}, update=update, upsert=upsert)
