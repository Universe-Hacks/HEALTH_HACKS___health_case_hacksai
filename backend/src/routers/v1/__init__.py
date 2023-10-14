from fastapi import APIRouter
from src.routers.v1.cities import router as cities_router

router = APIRouter(prefix="/v1")
router.include_router(cities_router)

__all__ = ("router",)
