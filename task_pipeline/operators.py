from collections.abc import Callable, Sequence
from typing import Any

from task_pipeline._utils import await_maybe
from task_pipeline.types_ import (
    IExecutable,
    IPipelineStage,
    MatchItem,
    P,
    T,
)


class Filter(IPipelineStage[P, Sequence[T]]):
    def __init__(
        self,
        stage: IExecutable[P, Sequence[Any]],
        by: Callable[[Any], T],
    ) -> None:
        self._stage = stage
        self._by = by

    async def __call__(self, value: P) -> Sequence[Any]:
        return [
            item for item in await await_maybe(self._stage(value)) if self._by(item)
        ]


class Check(IPipelineStage[P, T | P]):
    def __init__(
        self,
        stage: IExecutable[P, T],
        clause: Callable[[P], bool],
    ) -> None:
        self._stage = stage
        self._clause = clause

    async def __call__(self, value: P) -> T | P:
        if self._clause(value):
            return await await_maybe(self._stage(value))
        return value


class Match(IPipelineStage[P, T]):
    def __init__(
        self,
        *items: MatchItem[P, T],
        else_: IExecutable[P, T] | None = None,
    ) -> None:
        self._items = items
        self._else = else_

    async def __call__(self, value: P) -> T:
        for item in self._items:
            if item.clause(value):
                return await await_maybe(item.stage(value))

        if self._else is None:
            message = f"No match for {value}"
            raise ValueError(message)

        return await await_maybe(self._else(value))
