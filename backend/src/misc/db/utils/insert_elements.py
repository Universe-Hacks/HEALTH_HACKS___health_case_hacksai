from OSMPythonTools.element import Element

from src.db.models.osm_objects import ObjectType, OSMCoordinate, OSMMember, OSMObject
from src.db.repositories.osm_objects import OSMObjectsRepository


async def insert_elements(
    elements: list[Element],
    elements_type: ObjectType,
    city_name: str,
    region_name: str,
) -> None:
    osm_repo = OSMObjectsRepository()

    osm_objects = []

    for element in elements:
        try:
            members = [
                OSMMember(osm_id=member.id(), osm_type=member.type())
                for member in element.members()
            ]
        except Exception:
            members = []
        try:
            nodes = [node.id() for node in element.nodes()]
        except Exception:
            nodes = []

        osm_objects.append(
            OSMObject(
                osm_id=element.id(),
                osm_type=element.type(),
                object_type=elements_type,
                city=city_name,
                district=region_name,
                tags=element.tags(),
                coordinate=OSMCoordinate(
                    latitude=element.centerLat() or element.lat(),
                    longitude=element.centerLon() or element.lon(),
                ),
                members=members or None,
                nodes=nodes or None,
            ),
        )

    await osm_repo.insert_many(osm_objects)
