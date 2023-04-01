from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    SCHEDULE_URL: str
    CHUNK_SIZE_BYTES: int = 10240
    MAX_SAVE_SCHEDULE_FILES_WORKERS: int = 10
    SAVE_SCHEDULE_FILES_DIR: str = 'tmp/schedule_files'
