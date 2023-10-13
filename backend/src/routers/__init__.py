from fastapi import APIRouter

from src.routers.v1 import router as v1_router


def build_routers() -> APIRouter:
    router = APIRouter(prefix="/api")
    router.include_router(v1_router)
    return router


__all__ = ("build_routers",)
