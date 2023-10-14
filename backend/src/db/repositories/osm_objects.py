from typing import TypeAlias, Annotated

from fastapi import Depends

from src.db.models.osm_objects import OSMObject
from src.db.repositories.base_repository import BaseRepository


class OSMObjectsRepository(BaseRepository[OSMObject]):
    database_name = "osm"
    collection_name = "objects"
    model = OSMObject

    async def count_tag_by_cities(self, tag: str) -> list:
        pipeline = [
            {"$match": {f"tags.{tag}": {"$exists": True}}},
            {
                "$group": {
                    "_id": {"city": "$city", f"{tag}": f"$tags.{tag}"},
                    "counter": {"$sum": 1},
                },
            },
            {
                "$project": {
                    "_id": 0,
                    "city": "$_id.city",
                    f"{tag}": f"$_id.{tag}",
                    "count": "$counter",
                },
            },
        ]
        return await self._execute_aggregation(pipeline)

    async def count_types_by_cities(self) -> list:
        pipeline = [
            {
                "$group": {
                    "_id": {"city": "$city", "type": "$object_type"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "city": "$_id.city",
                    "type": "$_id.type",
                    "count": "$count",
                }
            },
        ]
        return await self._execute_aggregation(pipeline)


InjectOSMObjectsRepository: TypeAlias = Annotated[OSMObjectsRepository, Depends()]
