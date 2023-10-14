from typing import Annotated, TypeAlias

from fastapi import Depends

from src.db.models.osm_objects import OSMObject
from src.db.repositories.base_repository import BaseRepository


class OSMObjectsRepository(BaseRepository[OSMObject]):
    database_name = "osm"
    collection_name = "objects"
    model = OSMObject

    async def count_tag(
        self,
        tag: str,
        *,
        by_district: bool = False,
    ) -> list[dict[str, str | int]]:
        group = {
            "$group": {
                "_id": {"city": "$city", f"{tag}": f"$tags.{tag}"},
                "counter": {"$sum": 1},
            },
        }

        project = {
            "$project": {
                "_id": 0,
                "city": "$_id.city",
                f"{tag}": f"$_id.{tag}",
                "count": "$counter",
            },
        }
        if by_district:
            group["$group"]["_id"]["district"] = "$district"
            project["$project"]["district"] = "$_id.district"

        pipeline = [
            {"$match": {f"tags.{tag}": {"$exists": True}}},
            group,
            project,
        ]
        return await self._execute_aggregation(pipeline)

    async def count_types(
        self,
        *,
        by_district: bool = False,
    ) -> list[dict[str, str | int]]:
        group = {
            "$group": {
                "_id": {"city": "$city", "type": "$object_type"},
                "count": {"$sum": 1},
            }
        }
        project = {
            "$project": {
                "_id": 0,
                "city": "$_id.city",
                "type": "$_id.type",
                "count": "$count",
            }
        }
        if by_district:
            group["$group"]["_id"]["district"] = "$district"
            project["$project"]["district"] = "$_id.district"
        return await self._execute_aggregation([group, project])


InjectOSMObjectsRepository: TypeAlias = Annotated[OSMObjectsRepository, Depends()]
