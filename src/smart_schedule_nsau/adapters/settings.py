from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    IS_DEV_MODE: bool = False
