from fastapi import APIRouter

from src.routers.v1.status import router as status_router

router = APIRouter(prefix="/v1")
router.include_router(status_router)

__all__ = ("router",)
