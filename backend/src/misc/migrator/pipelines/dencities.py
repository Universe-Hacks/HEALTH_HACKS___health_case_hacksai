from collections import defaultdict
from typing import Any

from src.db.models.city.city_model import CityModel, ObjectDensity, TypeDensity
from src.db.models.city.district import DistrictModel
from src.db.models.osm_objects import OSMCoordinate
from src.db.repositories.city import CityRepository
from src.db.repositories.osm_objects import OSMObjectsRepository
from src.misc.gis.dto import CoordinateDTO
from src.misc.migrator.parser import OSMParser
from src.services.metrics import MetricsService


class DensitiesMigrationPipeline:
    def __init__(self):
        self.parser = OSMParser()
        self.osm_object_repository = OSMObjectsRepository()
        self.metrics_service = MetricsService()

    async def _get_tag_densities_city(
        self,
        area_by_city: dict[str, float],
        tags: list[str],
    ) -> defaultdict[Any, dict]:
        tag_densities_city = defaultdict(dict)
        for tag in tags:
            print(f"Counting {tag}")
            for tag_info in await self.osm_object_repository.count_tag(tag):
                city = tag_info["city"]
                tag_densities_city[city][tag_info[tag]] = (
                    tag_info["count"] / area_by_city[city]
                )
        return tag_densities_city

    async def _get_type_densities_city(
        self,
        area_by_city: dict[str, float],
    ) -> defaultdict[Any, dict]:
        type_densities_city = defaultdict(dict)
        for type_info in await self.osm_object_repository.count_types():
            city = type_info["city"]
            type_densities_city[city][type_info["type"]] = (
                type_info["count"] / area_by_city[city]
            )
        return type_densities_city

    async def _get_tag_districts_by_city(
        self,
        district_areas: dict[str, dict[str, float]],
        tags: list[str],
    ) -> defaultdict[Any, dict]:
        tag_districts_by_city = defaultdict(lambda: defaultdict(dict))
        for tag in tags:
            for district_info in await self.osm_object_repository.count_tag(
                tag, by_district=True
            ):
                city = district_info["city"]
                district = district_info["district"]

                tag_districts_by_city[city][district][district_info[tag]] = (
                    district_info["count"] / district_areas[city][district]
                )
        return tag_districts_by_city

    async def _get_type_districts_by_city(
        self,
        district_areas: dict[str, dict[str, float]],
    ) -> defaultdict[Any, dict]:
        type_districts_by_city = defaultdict(lambda: defaultdict(dict))
        for type_info in await self.osm_object_repository.count_types(by_district=True):
            city = type_info["city"]
            district = type_info["district"]

            type_districts_by_city[city][district][type_info["type"]] = (
                type_info["count"] / district_areas[city][district]
            )
        return type_districts_by_city

    async def _get_positivity_by_district(self) -> defaultdict[Any, dict]:
        positivity_by_district = defaultdict(lambda: defaultdict(dict))
        positivity_info = (
            await self.osm_object_repository.calculate_positivity_rate_by_district()
        )
        for row in positivity_info:
            city = row["city"]
            district = row["district"]
            positivity_by_district[city][district] = row["rate"]

        return positivity_by_district

    async def _get_cities_coordinates(
        self,
        cities: list[str],
    ) -> dict[str, CoordinateDTO]:
        cities_coordinates = {}
        for city in cities:
            city_coord = self.parser.parse_city_coordinate(city_name=city)
            cities_coordinates[city] = city_coord
        return cities_coordinates

    @staticmethod
    async def _get_districts_coordinates(
        cities: list[str],
    ) -> dict[str, dict[str, list[dict[str, float]]]]:
        result = {}
        for city in cities:
            districts_coordinates = {
                district["tags"]["name"]: [
                    coords
                    for member in district["members"]
                    for coords in member["geometry"]
                ]
                for district in [r._json for r in OSMParser.parse_regions(city)]
            }
            result[city] = districts_coordinates
        return result

    async def execute(
        self,
        area_by_city: dict[str, float],
        district_areas: dict[str, dict[str, float]],
    ) -> None:
        print("Migrating densities")
        tags = ["amenity", "shop", "leisure", "highway"]
        districts_coordinates = await self._get_districts_coordinates(
            list(area_by_city.keys())
        )
        tag_densities_city = await self._get_tag_densities_city(area_by_city, tags)
        type_densities_city = await self._get_type_densities_city(area_by_city)
        tag_districts_by_city = await self._get_tag_districts_by_city(
            district_areas,
            tags,
        )
        type_districts_by_city = await self._get_type_districts_by_city(district_areas)
        positivity_by_district = await self._get_positivity_by_district()
        cities_coordinates = await self._get_cities_coordinates(
            list(area_by_city.keys())
        )
        docs = [
            CityModel(
                name=city,
                area=area,
                coordinate=OSMCoordinate(
                    latitude=cities_coordinates[city].latitude,
                    longitude=cities_coordinates[city].longitude,
                ),
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
                        polygon_coordinates=[
                            OSMCoordinate(
                                latitude=coord["lat"],
                                longitude=coord["lon"],
                            )
                            for coord in districts_coordinates[city][district]
                        ],
                        negative_points_overflow=(
                            await self.metrics_service.calculate_negative_points_overflow(
                                city, district
                            )
                        ),
                        min_negative_point_distance=(
                            await self.metrics_service.calculate_min_negative_point_distance(
                                city, district
                            )
                        ),
                    )
                    for district, area in district_areas[city].items()
                ],
                avg_negatives_distance=(
                    await self.metrics_service.calculate_avg_negatives_distance(city)
                ),
            )
            for city, area in area_by_city.items()
        ]
        city_info_repo = CityRepository()
        await city_info_repo.insert_many(docs)
