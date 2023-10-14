from src.db.models.object_density import ObjectDensity
from src.db.repositories.base_repository import BaseRepository


class ObjectDensityRepository(BaseRepository):
    model = ObjectDensity
    database_name = "osm"
    collection_name = "object_density"
