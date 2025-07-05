import abc

from app.internal.types import AnyType, HasKeyAndSerializable


class Storage(abc.ABC):
    @abc.abstractmethod
    def get(self, *, key: AnyType) -> AnyType:
        """Получить состояние из хранилища."""
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, *dtos: HasKeyAndSerializable) -> None:
        """Сохранить состояние в хранилище."""
        raise NotImplementedError


class Queue(abc.ABC):
    @abc.abstractmethod
    def push(self, key: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def pop(self, timeout: int = 0) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def pop_all(self) -> list[str]:
        raise NotImplementedError
