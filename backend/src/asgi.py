import uvicorn
from fastapi import FastAPI

from src.routers import build_routers

app = FastAPI()

app.include_router(build_routers())

if __name__ == "__main__":
    uvicorn.run("src.asgi:app", host="0.0.0.0", port=80, reload=True)
