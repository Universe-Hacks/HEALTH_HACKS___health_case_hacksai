from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class _Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"


settings = _Settings()  # pylint: disable=W0612
