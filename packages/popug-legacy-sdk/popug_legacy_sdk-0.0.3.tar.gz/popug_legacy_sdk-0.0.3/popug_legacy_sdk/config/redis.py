from pydantic import BaseModel


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 1
    redis_pool_name: str = "default"

    @property
    def get_redis_url(self):
        return f"redis://{self.host}:{self.port}/{self.db}"
