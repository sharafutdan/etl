import logging
from datetime import datetime
from typing import Iterator
from tenacity import retry, wait_random_exponential, before_sleep_log
from elasticsearch import Elasticsearch, helpers
from app.telemetry.logger import logger
from app.core.domain.movie.dto import MovieDTO
from app.core.storage.abc import Storage, Queue
from app.internal.types import Command, AnyType, LastSyncTimeProvider


def serialize(dto: MovieDTO) -> dict[str, AnyType]:
    return {"_index": "movies", "_id": dto.id, "_source": dto.serialize()}


class SetMovieLastSyncTimeCommand(Command[datetime, None]):
    def __init__(self, last_sync_time_provider: LastSyncTimeProvider):
        self._provider = last_sync_time_provider

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def process(self, value: datetime) -> None:
        self._provider.set_last_sync_time(value)


class SaveMovieToStorageCommand(Command[MovieDTO, None]):
    def __init__(
        self,
        log: logging.Logger,
        storage: Storage,
    ) -> None:
        self._logger = log
        self._storage = storage

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def process(self, value: MovieDTO) -> None:
        self._logger.info("Сохранение фильма {}".format(value.id))
        self._storage.save(value)


class PushMovieToQueueCommand(Command[MovieDTO, None]):
    def __init__(
        self,
        queue: Queue,
    ) -> None:
        self._queue = queue

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def process(self, value: MovieDTO) -> None:
        self._queue.push(key=value.key)


class SendMovieToElasticSearchCommand(Command[Iterator[MovieDTO], None]):
    def __init__(
        self,
        log: logging.Logger,
        client: Elasticsearch,
    ) -> None:
        self._logger = log
        self._client = client
        self._bulk = helpers.bulk

    @retry(
        wait=wait_random_exponential(multiplier=1, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def process(self, value: Iterator[MovieDTO]) -> None:
        actions = []
        for movie in value:
            self._logger.info("Отправка фильма в индекс {}".format(movie.id))
            actions.append(serialize(movie))
        self._bulk(client=self._client, actions=actions)
