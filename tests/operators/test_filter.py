from typing import cast

import pytest
from task_pipeline.operators import Filter
from task_pipeline.pipe import Collect

pytestmark = [pytest.mark.anyio]


def pow_(x: int, n: int) -> int:
    return cast(int, x**n)


async def test_ok() -> None:
    collect: Collect[int] = Collect(
        lambda x: pow_(x, 1),
        lambda x: pow_(x, 2),
        lambda x: pow_(x, 3),
    )
    pipe = Filter(
        collect,
        by=lambda x: x > 0,
    )

    assert await pipe(-1) == [1]
