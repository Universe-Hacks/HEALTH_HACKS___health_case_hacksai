from typing import Annotated, Any, TypeAlias

from OSMPythonTools.overpass import Overpass
from fastapi import Depends


class OSMService:
    def __init__(self):
        self.overpass = Overpass()

    def get_positive(self, city_name: str) -> Any:
        return self.overpass.query(
            f"""
                area["name"="{city_name}"]->.searchArea;
                (
                 // Парки, открытые зеленые площадки
                  node(area.searchArea)["leisure"="park"];
                  way(area.searchArea)["leisure"="park"];
                  relation(area.searchArea)["leisure"="park"];

                  // Пешеходные дорожки, тротуары
                  // node(area.searchArea)["highway"="footway"];
                  //way(area.searchArea)["highway"="footway"];
                  // relation(area.searchArea)["highway"="footway"];

                  // Спортивная площадка, поле для различных игр
                  node(area.searchArea)["leisure"="pitch"];
                  way(area.searchArea)["leisure"="pitch"];
                  relation(area.searchArea)["leisure"="pitch"];

                  // Спортивный центр
                  node(area.searchArea)["leisure"="sports_centre"];
                  way(area.searchArea)["leisure"="sports_centre"];
                  relation(area.searchArea)["leisure"="sports_centre"];

                  // Крупные стадионы
                  node(area.searchArea)["leisure"="stadium"];
                  way(area.searchArea)["leisure"="stadium"];
                  relation(area.searchArea)["leisure"="stadium"];

                  // Дорожки: беговые, велосипедные, конно-спортивные
                  node(area.searchArea)["leisure"="track"];
                  way(area.searchArea)["leisure"="track"];
                  relation(area.searchArea)["leisure"="track"];

                  // Рынок, базар
                  // node(area.searchArea)["shop"="market"];
                  // way(area.searchArea)["shop"="market"];
                  // relation(area.searchArea)["shop"="market"];

                  // Специализированный магазин, продающий свежие фрукты и овощи
                  node(area.searchArea)["shop"="greengrocer"];
                  way(area.searchArea)["shop"="greengrocer"];
                  relation(area.searchArea)["shop"="greengrocer"];

                  // Фермерские магазины
                  node(area.searchArea)["shop"="farm"];
                  way(area.searchArea)["shop"="farm"];
                  relation(area.searchArea)["shop"="farm"];
                );
                out center;
            """,
        )

    def get_negative(self, city_name: str) -> Any:
        return self.overpass.query(
            f"""
                area["name"="{city_name}"]->.searchArea;
                (
                 // Магазины, специализирующиеся на продаже электронных сигарет и аксессуаров к ним
                  node(area.searchArea)["shop"="tobacco"];
                  way(area.searchArea)["shop"="tobacco"];
                  relation(area.searchArea)["shop"="tobacco"];

                  // Магазины, продающие табак, сигареты и принадлежности к ним
                  node(area.searchArea)["shop"="smoke_shop"];
                  way(area.searchArea)["shop"="smoke_shop"];
                  relation(area.searchArea)["shop"="smoke_shop"];

                  // Точки продажи алкоголя
                  node(area.searchArea)["amenity"="bar"];
                  way(area.searchArea)["amenity"="bar"];
                  relation(area.searchArea)["amenity"="bar"];

                  node(area.searchArea)["amenity"="pub"];
                  way(area.searchArea)["amenity"="pub"];
                  relation(area.searchArea)["amenity"="pub"];

                  node(area.searchArea)["shop"="wine"];
                  way(area.searchArea)["shop"="wine"];
                  relation(area.searchArea)["shop"="wine"];

                  node(area.searchArea)["shop"="alcohol"];
                  way(area.searchArea)["shop"="alcohol"];
                  relation(area.searchArea)["shop"="alcohol"];

                  node(area.searchArea)["amenity"="fast_food"];
                  way(area.searchArea)["amenity"="fast_food"];
                  relation(area.searchArea)["amenity"="fast_food"];

                  node(area.searchArea)["amenity"="food_court"];
                  way(area.searchArea)["amenity"="food_court"];
                  relation(area.searchArea)["amenity"="food_court"];
                );
                out center;
            """,
        )

    def get_studies(self, city_name: str) -> Any:
        return self.overpass.query(
            f"""
                area["name"="{city_name}"]->.searchArea;
                (
                 // BY3 (Высшее учебное заведение)
                  node(area.searchArea)["amenity"="university"];
                  way(area.searchArea)["amenity"="university"];
                  relation(area.searchArea)["amenity"="university"];

                  // Колледж, техникум, профессиональный лицей, училище
                  node(area.searchArea)["amenity"~"college|technical_college|professional_college|vocational_school"];
                  way(area.searchArea)["amenity"~"college|technical_college|professional_college|vocational_school"];
                  relation(area.searchArea)["amenity"~"college|technical_college|professional_college|vocational_school"];

                  // Среднее общеобразовательное учебное заведение, начальная или средняя школа, гимназия, лицей
                  node(area.searchArea)["amenity"~"school|primary|secondary|gymnasium|lyceum"];
                  way(area.searchArea)["amenity"~"school|primary|secondary|gymnasium|lyceum"];
                  relation(area.searchArea)["amenity"~"school|primary|secondary|gymnasium|lyceum"];

                  // Детский сад
                  node(area.searchArea)["amenity"="kindergarten"];
                  way(area.searchArea)["amenity"="kindergarten"];
                  relation(area.searchArea)["amenity"="kindergarten"];

                  // Языковая школа
                  node(area.searchArea)["amenity"="language_school"];
                  way(area.searchArea)["amenity"="language_school"];
                  relation(area.searchArea)["amenity"="language_school"];

                  // Музыкальная школа
                  node(area.searchArea)["amenity"="music_school"];
                  way(area.searchArea)["amenity"="music_school"];
                  relation(area.searchArea)["amenity"="music_school"];
                );
                out center;
            """,
        )

    def get_regions(self, city_name: str) -> Any:
        return self.overpass.query(
            f"""
                area["name"="{city_name}"]->.searchArea;
                (
                 // Выбрать административные границы (районы)
                  rel(area.searchArea)["boundary"="administrative"]["admin_level"="9"];
                );
                out geom;
            """,
        )

    def get_city(self, city_name: str) -> Any:
        return self.overpass.query(
            f"""
            node["place"="city"]["name"="{city_name}"];
            out center;
            """
        )


InjectOSMService: TypeAlias = Annotated[OSMService, Depends()]
