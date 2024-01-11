import dataclasses
from collections.abc import Awaitable, Callable
from typing import Generic, Protocol, TypeVar

P = TypeVar("P")
P_contra = TypeVar("P_contra", contravariant=True)
T_co = TypeVar("T_co", covariant=True)
T = TypeVar("T")
IExecutable = Callable[[P], T | Awaitable[T]]

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")


class IPipelineStage(Protocol[P_contra, T_co]):
    async def __call__(self, value: P_contra) -> T_co:
        ...


@dataclasses.dataclass(slots=True, frozen=True, kw_only=True)
class MatchItem(Generic[P, T]):
    stage: IExecutable[P, T]
    clause: Callable[[P], bool]
