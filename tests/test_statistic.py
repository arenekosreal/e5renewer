"""Test e5renewer.processor.statistic functions and classes."""

import pytest
from e5renewer.config import User
from e5renewer.processor.statistic import invoke
from e5renewer.processor.statistic import get_user_results
from e5renewer.processor.statistic import set_user_running
from e5renewer.processor.statistic import get_running_users
from e5renewer.processor.statistic import get_waiting_users
from e5renewer.processor.statistic import set_api_call_result


@pytest.mark.asyncio()
async def test_set_user_running(user: User):
    """Check if set_user_running is correct."""
    set_user_running(user, True)
    assert user.name in await get_running_users()
    set_user_running(user, False)
    assert user.name in await get_waiting_users()


@pytest.mark.asyncio()
async def test_user_results(user: User):
    """Check if get_user_results is correct."""
    set_api_call_result(user.name, "Pytest.Test", "200 - OK")
    assert "200 - OK" in await get_user_results(user.name, "Pytest.Test")
    assert "200 - OK" in await invoke("get_user_results", user=user.name, api_name="Pytest.Test")
