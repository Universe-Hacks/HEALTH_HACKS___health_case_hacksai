import asyncio

from src.db.models.osm_objects import ObjectType
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.gis.distance import calculate_distance_in_meters


class MetricsService:
    def __init__(self):
        self.osm_objects_repository = OSMObjectsRepository()

    async def calculate_avg_negatives_distance(self, city_name: str) -> float:
        negative_points = await self.osm_objects_repository.find(
            {"object_type": ObjectType.NEGATIVE, "city": city_name}
        )
        positive_points = await self.osm_objects_repository.find(
            {"object_type": ObjectType.POSITIVE, "city": city_name}
        )

        total_distance = 0
        count = 0
        for negative_point in negative_points:
            for positive_point in positive_points:
                total_distance += calculate_distance_in_meters(
                    negative_point.coordinate,
                    positive_point.coordinate,
                )
                count += 1

        return total_distance / count if count > 0 else 0

    async def calculate_negative_points_overflow(
        self, city_name: str, district_name: str
    ) -> int:
        negative_points = await self.osm_objects_repository.find(
            {
                "object_type": ObjectType.NEGATIVE,
                "city": city_name,
                "district": district_name,
            }
        )
        positive_points = await self.osm_objects_repository.find(
            {
                "object_type": ObjectType.POSITIVE,
                "city": city_name,
                "district": district_name,
            }
        )
        overflow_counter = 0
        for negative_point in negative_points:
            for positive_point in positive_points:
                if (
                    calculate_distance_in_meters(
                        negative_point.coordinate,
                        positive_point.coordinate,
                    )
                    < 100
                ):
                    overflow_counter += 1
        return overflow_counter


# async def main():
#     ms = MetricsService()
#     print(await ms.calculate_avg_negatives_distance("Екатеринбург"))
#     print(await ms.calculate_negative_points_overflow("Екатеринбург", "Октябрьский"))
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
