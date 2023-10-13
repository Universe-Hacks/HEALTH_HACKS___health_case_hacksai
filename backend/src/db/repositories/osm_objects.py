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
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "city": "$_id.city",
                    f"{tag}": f"$_id.{tag}",
                    "count": "$counter",
                }
            },
        ]
        docs = []
        async for doc in self.collection.aggregate(pipeline):
            docs.append(doc)
        return docs
