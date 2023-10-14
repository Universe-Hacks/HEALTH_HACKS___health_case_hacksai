import asyncio
from collections import defaultdict
import json
import logging

from src.db.models.city.city_model import CityModel, ObjectDensity, TypeDensity
from src.db.models.city.district import DistrictModel
from src.db.models.osm_objects import ObjectType
from src.db.repositories.city import CityRepository
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.db.utils.insert_elements import insert_elements
from src.misc.db.utils.parse_elements import parse_elements

logger = logging.getLogger(__name__)


async def migrate_osm_objects(cities: list[str]):
    print("Migrating osm objects")
    for city_name in cities:
        print(f"Migrating {city_name}")
        elements = parse_elements(city_name)
        try:
            await insert_elements(elements.positive, ObjectType.POSITIVE, city_name)
            await insert_elements(elements.negative, ObjectType.NEGATIVE, city_name)
            await insert_elements(elements.studies, ObjectType.STUDY, city_name)
        except TypeError:
            print(f"Error! No elements for {city_name}")


async def migrate_densities(
    area_by_city: dict[str, float],
    district_areas: dict[str, dict[str, float]],
) -> None:
    print("Migrating densities")
    osm_objects_repo = OSMObjectsRepository()
    tags = ["amenity", "shop", "leisure", "highway"]

    # Fill density_by_object
    tag_densities_city = defaultdict(dict)
    for tag in tags:
        print(f"Counting {tag}")
        for tag_info in await osm_objects_repo.count_tag(tag):
            city = tag_info["city"]
            tag_densities_city[city][tag_info[tag]] = (
                tag_info["count"] / area_by_city[city]
            )

    # Fill density_by_type
    type_densities_city = defaultdict(dict)
    for type_info in await osm_objects_repo.count_types():
        city = type_info["city"]
        type_densities_city[city][type_info["type"]] = (
            type_info["count"] / area_by_city[city]
        )

    # Fill density_by_object by district
    tag_districts_by_city = defaultdict(lambda: defaultdict(dict))
    for tag in tags:
        for district_info in await osm_objects_repo.count_tag(tag, by_district=True):
            city = district_info["city"]
            district = district_info["district"]

            tag_districts_by_city[city][district][district_info[tag]] = (
                district_info["count"] / district_areas[city][district]
            )

    # Fill density_by_type by district
    type_districts_by_city = defaultdict(lambda: defaultdict(dict))
    for type_info in await osm_objects_repo.count_types(by_district=True):
        city = type_info["city"]
        district = type_info["district"]

        type_districts_by_city[city][district][type_info["type"]] = (
            type_info["count"] / district_areas[city][district]
        )

    docs = [
        CityModel(
            name=city,
            area=area,
            density_by_object=ObjectDensity(**tag_densities_city[city]),
            density_by_type=TypeDensity(**type_densities_city[city]),
            districts=[
                DistrictModel(
                    name=district,
                    area=area,
                    density_by_object=ObjectDensity(
                        **tag_districts_by_city[city][district]
                    ),
                    density_by_type=TypeDensity(
                        **type_districts_by_city[city][district]
                    ),
                )
                for district, area in district_areas[city].items()
            ],
        )
        for city, area in area_by_city.items()
    ]
    city_info_repo = CityRepository()
    await city_info_repo.insert_many(docs)


async def main():
    with open("areas_by_hacked_city.json") as file:
        district_areas = json.load(file)
    with open("areas_hack.json") as file:
        areas_json = json.load(file)

    await migrate_osm_objects(list(areas_json.keys()))
    await migrate_densities(areas_json, district_areas)


if __name__ == "__main__":
    asyncio.run(main())
