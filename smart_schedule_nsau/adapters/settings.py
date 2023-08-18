import pytz
from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    IS_DEV_MODE: bool = False
    TIME_ZONE: str

    @property
    def TZ_INFO(self) -> pytz.timezone:
        return pytz.timezone(self.TIME_ZONE)
