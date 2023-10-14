import asyncio
import json
import logging

from src.misc.migrator.pipelines.dencities import DensitiesMigrationPipeline

logger = logging.getLogger(__name__)


async def main():
    with open("files/areas_by_hacked_city.json") as file:
        district_areas = json.load(file)
    with open("files/areas_hack.json") as file:
        areas_json = json.load(file)

    await OSMObjectsMigrationPipeline().execute(city_names=list(areas_json.keys()))
    await DensitiesMigrationPipeline().execute(
        area_by_city=areas_json,
        district_areas=district_areas,
    )


if __name__ == "__main__":
    asyncio.run(main())
