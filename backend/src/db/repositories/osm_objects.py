from src.db.models.osm_objects import OSMObject
from src.db.repositories.base_repository import BaseRepository


class OSMObjectsRepository(BaseRepository[OSMObject]):
    database_name = "osm"
    collection_name = "objects"
    model = OSMObject
