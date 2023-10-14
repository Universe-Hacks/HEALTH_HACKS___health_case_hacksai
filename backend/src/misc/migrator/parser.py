from dataclasses import dataclass

from OSMPythonTools.element import Element

from src.misc.gis.dto import CoordinateDTO
from src.services.osm import OSMService


@dataclass(frozen=True, slots=True)
class ElementsDTO:
    positive: list[Element]
    negative: list[Element]
    studies: list[Element]


class OSMParser:
    @staticmethod
    def parse_elements(city_name: str) -> ElementsDTO:
        osm = OSMService()

        positive_elements = osm.get_positive(city_name).elements()
        negative_elements = osm.get_negative(city_name).elements()
        studies_elements = osm.get_studies(city_name).elements()

        return ElementsDTO(
            positive=positive_elements,
            negative=negative_elements,
            studies=studies_elements,
        )

    @staticmethod
    def parse_regions(city_name: str) -> list[Element]:
        osm = OSMService()
        return osm.get_regions(city_name).elements()

    @staticmethod
    def parse_city_coordinate(city_name: str) -> CoordinateDTO:
        osm = OSMService()
        city = osm.get_city(city_name).elements()[0]
        return CoordinateDTO(
            latitude=city.lat(),
            longitude=city.lon(),
        )
