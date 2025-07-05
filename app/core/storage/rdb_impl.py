from datetime import datetime
from typing import Any
from app.core.storage.abc import Storage, Queue
from app.telemetry.logger import logger
from app.internal.types import HasKeyAndSerializable
from redis import Redis


class MovieLastSyncTimeProvider:
    def __init__(
        self,
        redis: Redis,
    ) -> None:
        self._redis = redis

    def get_last_sync_time(self) -> datetime | None:
        sync_time: bytes = self._redis.get(name="movies:last-sync-time")
        if sync_time:
            return datetime.fromisoformat(sync_time.decode())
        return None

    def set_last_sync_time(self, dt: datetime) -> datetime:
        self._redis.set(name="movies:last-sync-time", value=dt.isoformat())
        return dt


class RedisStorage(Storage):
    def __init__(self, *, redis: Redis) -> None:
        self._redis = redis

    def get(self, *, key: str) -> dict[str, Any]:
        return self._redis.get(name=key)

    def save(self, *dtos: HasKeyAndSerializable) -> None:
        pipe = self._redis.pipeline()
        for dto in dtos:
            pipe.set(name=dto.key, value=dto.serialize())
        pipe.execute()


class RedisQueue(Queue):
    def __init__(self, redis: Redis, queue_name: str = "movies:to-update"):
        self._redis = redis
        self._queue_name = queue_name

    def push(self, key: str) -> None:
        logger.info("Фильм на обновление {}".format(key))
        self._redis.lpush(self._queue_name, key)

    def pop(self, timeout: int = 0) -> str | None:
        result = self._redis.brpop(keys=self._queue_name, timeout=timeout)
        if result:
            _, key = result
            return key.decode()
        return None

    def pop_all(self) -> list[str]:
        keys = self._redis.lrange(name=self._queue_name, start=0, end=-1)
        self._redis.delete(self._queue_name)
        return [k.decode() for k in keys]
