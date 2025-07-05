import abc
from datetime import datetime
from typing import TypeVar, Protocol, Union, Any

from typing_extensions import Generic


NoneType = type(None)
TInput = TypeVar("TInput")
TResult = TypeVar("TResult")
AnyType = Any
DateTimeOrNone = Union[datetime, None]


class HasKeyAndSerializable(Protocol):
    def serialize(self) -> str: ...
    @property
    def key(self) -> AnyType: ...


class LastSyncTimeProvider(Protocol):
    def get_last_sync_time(self) -> datetime | None: ...
    def set_last_sync_time(self, dt: datetime) -> datetime: ...


class Command(Generic[TInput, TResult], abc.ABC):
    @abc.abstractmethod
    def process(self, value: TInput) -> TResult:
        raise NotImplementedError


class Query(
    Generic[TInput, TResult],
    abc.ABC,
):
    @abc.abstractmethod
    def execute(self, value: TInput) -> TResult:
        raise NotImplementedError
