import asyncio
from collections import defaultdict
import json
import logging

from pydantic import BaseModel

from src.db.models.city.city_model import CityModel, ObjectDensity, TypeDensity
from src.db.models.osm_objects import ObjectType
from src.db.repositories.city import CityRepository
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.db.utils.insert_elements import insert_elements
from src.misc.db.utils.parse_elements import parse_elements

logger = logging.getLogger(__name__)


class __CityArea(BaseModel):
    city: str
    area: float


async def migrate_areas() -> list[__CityArea]:
    logger.info("Migrating areas")
    with open("areas_hack.json") as file:
        areas_json = json.load(file)
    docs = [__CityArea(city=city, area=area) for city, area in areas_json.items()]
    return docs


async def migrate_osm_objects(cities: list[str]):
    logger.info("Migrating osm objects")
    for city_name in cities:
        logger.info(f"Migrating {city_name}")
        elements = parse_elements(city_name)
        try:
            await insert_elements(elements.positive, ObjectType.POSITIVE, city_name)
            await insert_elements(elements.negative, ObjectType.NEGATIVE, city_name)
            await insert_elements(elements.studies, ObjectType.STUDY, city_name)
        except TypeError:
            print(f"Error! No elements for {city_name}")


async def migrate_densities(area_by_city: dict[str, float]) -> None:
    logger.info("Migrating densities")
    osm_objects_repo = OSMObjectsRepository()
    tags = ["amenity", "shop", "leisure", "highway"]
    tag_densities_city = defaultdict(dict)
    for tag in tags:
        logger.info(f"Counting {tag}")
        for tag_info in await osm_objects_repo.count_tag_by_cities(tag):
            city = tag_info["city"]
            tag_densities_city[city][tag_info[tag]] = (
                tag_info["count"] / area_by_city[city]
            )

    type_densities_city = defaultdict(dict)

    for type_info in await osm_objects_repo.count_types_by_cities():
        city = type_info["city"]
        type_densities_city[city][type_info["type"]] = (
            type_info["count"] / area_by_city[city]
        )

    docs = [
        CityModel(
            city=city,
            area=area,
            density_by_object=ObjectDensity(**tag_densities_city[city]),
            density_by_type=TypeDensity(**type_densities_city[city]),
        )
        for city, area in area_by_city.items()
    ]
    city_info_repo = CityRepository()
    await city_info_repo.insert_many(docs)


async def main():
    city_areas = await migrate_areas()
    await migrate_osm_objects([doc.city for doc in city_areas])
    await migrate_densities({doc.city: doc.area for doc in city_areas})


if __name__ == "__main__":
    asyncio.run(main())
