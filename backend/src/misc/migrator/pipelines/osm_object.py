import asyncio
import logging

from OSMPythonTools.element import Element

from src.db.models.osm_objects import OSMCoordinate, OSMMember, OSMObject, ObjectType
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.gis.polygons import PolygonUtils
from src.misc.migrator.parser import ElementsDTO, OSMParser

logger = logging.getLogger(__name__)


class OSMObjectsMigrationPipeline:
    def __init__(self):
        self.parser = OSMParser()
        self.osm_repository = OSMObjectsRepository()

    async def _insert_elements_by_type(
        self,
        elements: list[Element],
        elements_type: ObjectType,
        city_name: str,
        region_name: str,
    ) -> None:
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

        await self.osm_repository.insert_many(osm_objects)

    async def insert_elements(
        self,
        region: Element,
        city_name: str,
        pos_list: list[Element],
        neg_list: list[Element],
        study_list: list[Element],
    ) -> None:
        print(f"Inserting city: {city_name} -> region: {region.tag('name')}")
        try:
            await self._insert_elements_by_type(
                elements=pos_list,
                elements_type=ObjectType.POSITIVE,
                city_name=city_name,
                region_name=region.tag("name"),
            )
            await self._insert_elements_by_type(
                elements=neg_list,
                elements_type=ObjectType.NEGATIVE,
                city_name=city_name,
                region_name=region.tag("name"),
            )
            await self._insert_elements_by_type(
                elements=study_list,
                elements_type=ObjectType.STUDY,
                city_name=city_name,
                region_name=region.tag("name"),
            )
        except TypeError as e:
            print(f"Error! {e}")

    async def migrate_city_region(
        self,
        region: Element,
        elements: ElementsDTO,
        city_name: str,
    ):
        print(f"Migrating city: {city_name} -> region: {region.tag('name')}")

        region_polygon = PolygonUtils.build_polygon_from_element(region)
        pos_list, neg_list, study_list = [], [], []
        for element in elements.positive:
            if region_polygon.contains_element(element):
                pos_list.append(element)
        for element in elements.negative:
            if region_polygon.contains_element(element):
                neg_list.append(element)
        for element in elements.studies:
            if region_polygon.contains_element(element):
                study_list.append(element)
        await self.insert_elements(
            region=region,
            city_name=city_name,
            pos_list=pos_list,
            neg_list=neg_list,
            study_list=study_list,
        )

    async def migrate_city(self, city_name: str):
        print(f"Migrating city: {city_name}")
        elements = OSMParser.parse_elements(city_name)
        regions = OSMParser.parse_regions(city_name)
        await asyncio.gather(
            *[
                self.migrate_city_region(region, elements, city_name)
                for region in regions
            ],
        )

    async def execute(self, city_names: list[str]):
        print(f"Migrating OSM objects for {len(city_names)} cities")
        await asyncio.gather(*[self.migrate_city(city_name) for city_name in city_names])
