from typing import Literal, NewType
from pydantic_settings import BaseSettings
import os

ElasticSearchDsn = NewType("ElasticSearchDsn", str)


class ElasticSearchSettings(BaseSettings):
    host: str = os.environ.get("ELASTICSEARCH_HOST", "localhost")
    port: int = os.environ.get("ELASTICSEARCH_PORT", 9200)
    proto: Literal["http", "https"] = os.environ.get("ELASTICSEARCH_PROTO", "http")

    @property
    def url(self) -> ElasticSearchDsn:
        return ElasticSearchDsn(f"{self.proto}://{self.host}:{self.port}")


settings = ElasticSearchSettings()
