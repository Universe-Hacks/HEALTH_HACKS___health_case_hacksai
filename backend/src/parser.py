import asyncio

from src.db.models.osm_objects import ObjectType
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.insert_elements import insert_elements
from src.misc.parse_elements import parse_elements


async def main():
    for city_name in ["Тамбов"]:
        elements = parse_elements(city_name)
        await insert_elements(elements.positive, ObjectType.POSITIVE, city_name)
        await insert_elements(elements.negative, ObjectType.NEGATIVE, city_name)
        await insert_elements(elements.studies, ObjectType.STUDY, city_name)


async def clear_mongo():
    osm_repo = OSMObjectsRepository()
    await osm_repo.collection.delete_many({})


if __name__ == "__main__":
    asyncio.run(main())
