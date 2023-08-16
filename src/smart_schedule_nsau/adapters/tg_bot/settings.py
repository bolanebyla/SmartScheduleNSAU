from pydantic import BaseSettings


class TgBotSettings(BaseSettings):
    TG_BOT_TOKEN: str
    LOGGING_LEVEL: str = 'INFO'

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'TeleBot': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False
                }
            }
        }

        return config
