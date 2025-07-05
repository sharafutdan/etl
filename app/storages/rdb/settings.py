import os

from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = os.environ.get("REDIS_HOST", "localhost")
    port: int = os.environ.get("REDIS_PORT", 6379)
    db: int = os.environ.get("REDIS_DB", 0)

    @property
    def url(self):
        return "redis://{}:{}/{}".format(self.host, self.port, self.db)


settings = RedisSettings()
