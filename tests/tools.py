import functools
import inspect
from collections.abc import Callable
from typing import ParamSpec, Protocol, TypeVar, cast
from unittest.mock import MagicMock

F_Spec = ParamSpec("F_Spec")
F_Return_co = TypeVar("F_Return_co", covariant=True)


class SpiedFunc(Protocol[F_Spec, F_Return_co]):
    @property
    def mock(self) -> MagicMock: ...

    def __call__(self, *args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return_co: ...


class SpiedAsyncFunc(Protocol[F_Spec, F_Return_co]):
    @property
    def mock(self) -> MagicMock: ...

    async def __call__(
        self, *args: F_Spec.args, **kwargs: F_Spec.kwargs
    ) -> F_Return_co: ...


def spy_decorator(
    method: Callable[F_Spec, F_Return_co],
) -> SpiedFunc[F_Spec, F_Return_co] | SpiedAsyncFunc[F_Spec, F_Return_co]:
    mock: MagicMock = MagicMock()

    if inspect.iscoroutinefunction(method):

        @functools.wraps(method)
        async def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return_co:  # pyright: ignore[reportRedeclaration]
            mock(*args, **kwargs)
            return await method(*args, **kwargs)

        wrapper.mock = mock  # pyright: ignore[reportAttributeAccessIssue]
        return cast("SpiedFunc[F_Spec, F_Return_co]", wrapper)

    else:  # noqa: RET505

        @functools.wraps(method)
        def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return_co:  # pyright: ignore[reportRedeclaration]
            mock(*args, **kwargs)
            return method(*args, **kwargs)

        wrapper.mock = mock  # pyright: ignore[reportAttributeAccessIssue]
        return cast("SpiedAsyncFunc[F_Spec, F_Return_co]", wrapper)
