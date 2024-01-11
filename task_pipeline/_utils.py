import inspect
from collections.abc import Awaitable

from task_pipeline.types_ import T


async def await_maybe(value: Awaitable[T] | T) -> T:
    if inspect.isawaitable(value):
        return await value  # type: ignore[no-any-return]
    return value  # type: ignore[return-value]
