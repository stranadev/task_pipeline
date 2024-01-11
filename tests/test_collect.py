import pytest
from task_pipeline.pipe import Collect, Pipe

pytestmark = [pytest.mark.anyio]


def _square(x: int) -> int:
    return x**2


async def test_collect() -> None:
    value = 12

    pipe = Collect(_square, _square, _square)

    assert await pipe(value) == [_square(value)] * 3


async def test_collect_with_pipe() -> None:
    value = 12
    pipe = Collect(Pipe(_square, str), _square, _square)

    assert await pipe(value) == [str(_square(value)), _square(value), _square(value)]
