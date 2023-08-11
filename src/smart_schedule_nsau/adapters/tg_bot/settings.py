from pydantic import BaseSettings


class TgBotSettings(BaseSettings):
    TG_BOT_TOKEN: str
