from pydantic import BaseSettings

from popug_legacy_sdk.config.auth import AuthSettings
from popug_legacy_sdk.config.redis import RedisSettings
from popug_legacy_sdk.config.database import DatabaseSettings


BASE_NAME = "POPUG_MARKET"


class Settings(BaseSettings):
    service: str = BASE_NAME
    # auth: AuthSettings
    # redis: RedisSettings
    # database: DatabaseSettings

    class Config:
        env_prefix = f"{BASE_NAME.upper()}_"
        env_file = "ci/.env"
        env_nested_delimiter = "__"


s = Settings()
# print(s)