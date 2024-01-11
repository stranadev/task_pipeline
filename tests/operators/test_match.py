import pytest
from task_pipeline.operators import Match
from task_pipeline.pipe import Pipe
from task_pipeline.types_ import MatchItem

pytestmark = [pytest.mark.anyio]


async def test_ok() -> None:
    value = 12
    match_stage = Match(
        MatchItem(
            stage=str,
            clause=lambda x: isinstance(x, int),
        ),
        MatchItem(
            stage=lambda x: str(x) * 10,
            clause=lambda x: isinstance(x, str),
        ),
    )

    pipe: Pipe[str] = Pipe(match_stage)

    assert await pipe(value) == str(value)
    assert await pipe(str(value)) == str(value) * 10


async def test_else_parameter() -> None:
    value = 12
    match_stage = Match(
        MatchItem(
            stage=str,
            clause=lambda x: isinstance(x, int),
        ),
        else_=lambda x: str(x) * 10,
    )

    pipe: Pipe[str] = Pipe(match_stage)

    assert await pipe(value) == str(value)
    assert await pipe(str(value)) == str(value) * 10


async def test_raise_else_parameter() -> None:
    match_stage = Match(
        MatchItem(
            stage=str,
            clause=lambda x: isinstance(x, int),
        ),
    )

    pipe: Pipe[str] = Pipe(match_stage)

    with pytest.raises(ValueError, match="No match"):
        await pipe("")
