from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CoordinateDTO:
    latitude: float
    longitude: float
