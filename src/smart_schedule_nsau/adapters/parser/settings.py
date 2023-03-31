from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    SCHEDULE_URL: str
    CHUNK_SIZE_BYTES = 10240
