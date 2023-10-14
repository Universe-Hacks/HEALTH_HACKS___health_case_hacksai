from typing import Self

from OSMPythonTools.element import Element
from shapely.geometry import Point, Polygon

from src.misc.gis.dto import CoordinateDTO


class PolygonUtils:
    def __init__(self, coordinates: list[CoordinateDTO]):
        self.polygon = Polygon([(c.longitude, c.latitude) for c in coordinates])

    @classmethod
    def build_polygon_from_element(cls, element: Element) -> Self:
        region_coordinates = []
        for m in element.__dict__["_json"]["members"]:
            for coordinate in m["geometry"]:
                region_coordinates.append(
                    CoordinateDTO(
                        latitude=coordinate["lat"],
                        longitude=coordinate["lon"],
                    )
                )
        return cls(region_coordinates)

    def contains(self, coordinate: CoordinateDTO) -> bool:
        point = Point(coordinate.longitude, coordinate.latitude)
        return self.polygon.contains(point)
