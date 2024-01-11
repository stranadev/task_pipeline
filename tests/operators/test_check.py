import pytest
from task_pipeline.operators import Check
from task_pipeline.pipe import Pipe

pytestmark = [pytest.mark.anyio]


async def test_ok() -> None:
    value = 12
    check: Check[str, int] = Check(
        int,
        lambda x: isinstance(x, str),
    )
    pipe: Pipe[str | int] = Pipe(
        str,
        check,
    )

    assert await pipe(value) == value


async def test_fail() -> None:
    value = 12
    check: Check[str, int] = Check(
        int,
        lambda x: isinstance(x, int),
    )
    pipe: Pipe[str | int] = Pipe(
        str,
        check,
    )

    assert await pipe(value) == str(value)
