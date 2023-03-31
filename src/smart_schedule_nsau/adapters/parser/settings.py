from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    SCHEDULE_URL: str
