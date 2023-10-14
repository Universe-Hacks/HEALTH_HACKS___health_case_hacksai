from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"


settings = _Settings()  # pylint: disable=W0612
