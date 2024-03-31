"""Test functions in e5renewer.processor."""

import pytest
from datetime import datetime
from datetime import timedelta
from e5renewer import processor
from e5renewer.config import User
from e5renewer.processor import main
from e5renewer.processor import stop
from e5renewer.processor import work
from e5renewer.processor import setup
from e5renewer.processor import sleep
from e5renewer.processor.statistic import invoke
from e5renewer.processor.statistic import set_api_call_result


@pytest.mark.asyncio()
async def test_sleep(user: User):
    """Check if sleep is correct."""
    user.from_time = datetime.now().time()
    user.to_time = (datetime.now() + timedelta(seconds=1)).time()
    await sleep(user)


@pytest.mark.asyncio()
async def test_work(user: User):
    """Check if work is correct."""
    setattr(processor, "_CALL_API_CALM_DOWN_MIN_SECS", 0)
    setattr(processor, "_CALL_API_CALM_DOWN_MAX_SECS", 1)
    await work(user)


@pytest.mark.asyncio()
async def test_main():
    """Check if main is correct."""
    await main(True)


@pytest.mark.asyncio()
async def test_exec_method_safe():
    """Check if exec_method_safe is correct."""
    set_api_call_result("pytest", "Pytest.Test", "200 - OK")
    assert "200 - OK" in await invoke("get_user_results", user="pytest", api_name="Pytest.Test")


def test_setup(user: User):
    """Check if setup is correct."""
    setup(user)


def test_stop():
    """Check if stop is correct."""
    stop()
