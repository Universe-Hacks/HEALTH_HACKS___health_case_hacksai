from fastapi import APIRouter
from src.routers.v1.cities import router as cities_router
from src.routers.v1.gis import router as gis_router

router = APIRouter(prefix="/v1")
router.include_router(cities_router)
router.include_router(gis_router)
__all__ = ("router",)
