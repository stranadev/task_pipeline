import pytest
from task_pipeline.pipe import Pipe

pytestmark = [pytest.mark.anyio]


def _square(x: int) -> int:
    return x**2


async def test_flat_pipe() -> None:
    pipeline = Pipe(_square, str)
    value = 12

    assert str(value**2) == await pipeline(value)


async def test_wrap_pipe() -> None:
    pipeline = Pipe(Pipe(_square), str)
    value = 12

    assert str(value**2) == await pipeline(value)
