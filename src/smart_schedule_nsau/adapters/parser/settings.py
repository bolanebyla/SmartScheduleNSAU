from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    SCHEDULE_URL: str
    CHUNK_SIZE_BYTES: int = 10240
    MAX_SAVE_SCHEDULE_FILES_WORKERS: int = 10
