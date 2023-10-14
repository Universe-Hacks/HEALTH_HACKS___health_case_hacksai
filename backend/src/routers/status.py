from fastapi import APIRouter

router = APIRouter(prefix="/status")


@router.get("")
async def status() -> dict[str, str]:
    return {"status": "ok"}
