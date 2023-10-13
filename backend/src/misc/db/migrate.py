import asyncio
from collections import defaultdict
import json

from src.db.models.city_area import CityArea
from src.db.repositories.city_area import CityAreaRepository
from db.models.object_density import ObjectDensity
from db.models.osm_objects import ObjectType
from db.repositories.object_density import ObjectDensityRepository
from db.repositories.osm_objects import OSMObjectsRepository
from misc.db.utils.insert_elements import insert_elements
from misc.db.utils.parse_elements import parse_elements


async def migrate_areas() -> list[CityArea]:
    with open("areas.json") as file:
        areas_json = json.load(file)
    docs = [CityArea(city=city, area=area) for city, area in areas_json.items()]
    repository = CityAreaRepository()
    # await repository.insert_many(docs)
    return docs


async def migrate_osm_objects(cities: list[str]):
    for city_name in cities:
        elements = parse_elements(city_name)
        try:
            await insert_elements(elements.positive, ObjectType.POSITIVE, city_name)
            await insert_elements(elements.negative, ObjectType.NEGATIVE, city_name)
            await insert_elements(elements.studies, ObjectType.STUDY, city_name)
        except TypeError:
            print(f"Error! No elements for {city_name}")


async def migrate_densities(area_by_city: dict[str, float]) -> None:
    osm_objects_repo = OSMObjectsRepository()
    tags = ["amenity", "shop", "leisure", "highway"]
    tags_by_city = defaultdict(dict)
    for tag in tags:
        for tag_info in await osm_objects_repo.count_tag_by_cities(tag):
            city = tag_info["city"]
            tags_by_city[city][tag_info[tag]] = tag_info["count"] / area_by_city[city]
    docs = [
        ObjectDensity(city=city, **tags_info) for city, tags_info in tags_by_city.items()
    ]
    object_density_repo = ObjectDensityRepository()
    await object_density_repo.insert_many(docs)


async def main():
    city_areas = await migrate_areas()
    # await migrate_osm_objects([doc.city for doc in city_areas])
    # await migrate_densities({doc.city: doc.area for doc in city_areas})


if __name__ == "__main__":
    asyncio.run(main())
