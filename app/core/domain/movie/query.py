from collections.abc import Iterator
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from tenacity import retry, wait_random_exponential, before_sleep_log
from app.core.domain.movie.dto import MovieDTO
from app.core.domain.movie.repository import GetUpdatedFilmsQueryBuilder
from app.core.storage.abc import Queue, Storage
import itertools
from app.internal.types import (
    Query,
    DateTimeOrNone,
    LastSyncTimeProvider,
)
from app.telemetry.logger import logger


class GetFilmsLastSyncTimeQuery(Query[None, DateTimeOrNone]):
    def __init__(
        self,
        last_sync_time_provider: LastSyncTimeProvider,
    ) -> None:
        self._last_sync_time_provider = last_sync_time_provider

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def execute(self, value: None = None) -> DateTimeOrNone:
        return self._last_sync_time_provider.get_last_sync_time()


class GetFilmsFromPostgresQuery(Query[datetime, Iterator[MovieDTO]]):
    def __init__(self, session: Session) -> None:
        self._session = session
        self._query_builder = GetUpdatedFilmsQueryBuilder

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def execute(self, value: datetime) -> Iterator[MovieDTO]:
        movies = self._session.execute(
            self._query_builder.build(
                after=value,
            )
        )

        for movie in movies:
            logger.info("Найден фильм: %s", movie[0])
            yield MovieDTO(**movie._mapping)


class GetMoviesFromQueueQuery(Query[None, Iterator[MovieDTO]]):
    def __init__(
        self,
        queue: Queue,
        storage: Storage,
    ) -> None:
        self._queue = queue
        self._storage = storage

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def execute(self, value: None = None) -> Iterator[MovieDTO]:
        for batch in itertools.batched(self._queue.pop_all(), n=1000):
            for movie_key in batch:
                movie = self._storage.get(key=movie_key)
                yield MovieDTO.model_validate_json(movie)
