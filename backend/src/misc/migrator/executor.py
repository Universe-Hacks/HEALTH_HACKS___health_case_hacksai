import asyncio
import json
import logging
from collections import defaultdict

from src.db.models.city.city_model import CityModel, ObjectDensity, TypeDensity
from src.db.models.city.district import DistrictModel
from src.db.repositories.city import CityRepository
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.migrator.pipelines.osm_object import OSMObjectsMigrationPipeline

logger = logging.getLogger(__name__)


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

    # Calculate positive rate
    positivity_by_district = defaultdict(lambda: defaultdict(dict))
    positivity_info = await osm_objects_repo.calculate_positivity_rate_by_district()
    for row in positivity_info:
        city = row["city"]
        district = row["district"]

        positivity_by_district[city][district] = row["rate"]

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
                    positivity_rate=positivity_by_district[city][district],
                )
                for district, area in district_areas[city].items()
            ],
        )
        for city, area in area_by_city.items()
    ]
    city_info_repo = CityRepository()
    await city_info_repo.insert_many(docs)


async def main():
    with open("files/areas_by_hacked_city.json") as file:
        district_areas = json.load(file)
    with open("files/areas_hack.json") as file:
        areas_json = json.load(file)

    await OSMObjectsMigrationPipeline().execute(city_names=list(areas_json.keys()))
    # await migrate_densities(areas_json, district_areas)


if __name__ == "__main__":
    asyncio.run(main())
