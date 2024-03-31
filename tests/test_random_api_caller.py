"""Test if e5renewer.processor.msapis.RandomAPICaller works."""

import pytest
from e5renewer.config import User
from e5renewer.defines import AUTHOR
from e5renewer.processor.msapis import RandomAPICaller


@pytest.fixture()
def random_caller(user: User) -> RandomAPICaller:
    """Generate a RandomAPICaller instance."""
    return RandomAPICaller(user)


def test_metadata(random_caller: RandomAPICaller):
    """Check if RandomAPICaller's metadata is correct."""
    assert random_caller.author == AUTHOR
    assert random_caller.name == "Random API caller"


@pytest.mark.asyncio()
async def test_call_next_api(random_caller: RandomAPICaller):
    """Check if RandomAPICaller's call_next_api is correct."""
    await random_caller.call_next_api()
