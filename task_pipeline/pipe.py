import typing
from collections.abc import Sequence
from typing import Any

from task_pipeline._utils import await_maybe
from task_pipeline.types_ import (
    A,
    B,
    C,
    IExecutable,
    IPipelineStage,
    P,
    P_contra,
    T,
)


class Pipe(IPipelineStage[Any, T]):
    @typing.overload
    def __init__(
        self,
        a: IExecutable[Any, T],
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        a: IExecutable[Any, A],
        b: IExecutable[A, T],
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        a: IExecutable[Any, A],
        b: IExecutable[A, B],
        c: IExecutable[B, T],
    ) -> None:
        ...

    @typing.overload
    def __init__(
        self,
        a: IExecutable[Any, A],
        b: IExecutable[A, B],
        c: IExecutable[B, C],
        d: IExecutable[C, T],
    ) -> None:
        ...

    def __init__(self, *tasks: IExecutable[Any, Any]) -> None:  # type: ignore[misc]
        self.tasks = tasks

    async def __call__(self, value: P_contra) -> T:
        iterator = iter(self.tasks)
        result = await await_maybe(next(iterator)(value))
        for task in iterator:
            result = await await_maybe(task(result))
        return result  # type: ignore[no-any-return]


class Collect(IPipelineStage[P, Sequence[Any]]):
    def __init__(self, *tasks: IExecutable[P, Any]) -> None:
        self.tasks = tasks

    async def __call__(self, value: P) -> Sequence[Any]:
        return [await await_maybe(task(value)) for task in self.tasks]
