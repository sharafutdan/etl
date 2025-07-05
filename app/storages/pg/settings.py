from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import sqlalchemy as sa


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    driver: str = "postgresql+psycopg2"
    name: str = "postgres"
    username: str = "postgres"
    password: SecretStr = "postgres"
    host: str = "localhost"
    port: int = 5432

    echo: bool = False
    pool_size: int = 5

    @property
    def url(self) -> sa.URL:
        return sa.URL.create(
            drivername=self.driver,
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.name,
        )


settings = DatabaseSettings()
