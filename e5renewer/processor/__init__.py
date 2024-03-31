"""Processor module for E5Renewer."""

import random
import signal
import asyncio
from typing import Any
from datetime import datetime
from datetime import timedelta
from e5renewer.config import User
from e5renewer.logger import info
from e5renewer.logger import debug
from e5renewer.processor.msapis import call_next_api
from e5renewer.processor.msapis import get_list_apis
from e5renewer.processor.statistic import invoke
from e5renewer.processor.statistic import set_user_running


_users: list[User] = []
_tasks_for_method: set[asyncio.Task[None]] = set()
_tasks_for_user: set[asyncio.Task[None]] = set()
_running = False
_CALL_API_CALM_DOWN_MIN_SECS = 300
_CALL_API_CALM_DOWN_MAX_SECS = 900


async def sleep(user: User):
    set_user_running(user, False)
    now = datetime.now().time()
    if now < user.from_time:
        now = datetime.combine(datetime.today(), now)
        from_time = datetime.combine(datetime.today(), user.from_time)
        delta = from_time - now
    elif now > user.to_time:
        now = datetime.combine(datetime.today(), now)
        target = datetime.combine(
            (datetime.today() + timedelta(days=1)).date(),  # tomorrow
            user.from_time,
        )
        delta = target - now
    else:
        delta = timedelta()
    secs = delta.total_seconds()
    if secs > 0:
        debug("Waiting for %fs to arrive start time...", secs)
        await asyncio.sleep(secs)


async def work(user: User):
    set_user_running(user, True)
    await call_next_api(user)
    sleep = random.uniform(
        _CALL_API_CALM_DOWN_MIN_SECS,
        _CALL_API_CALM_DOWN_MAX_SECS,
    )
    debug("Sleeping for %fs...", sleep)
    await asyncio.sleep(sleep)


async def _block(user: User):
    while _running:
        if user.is_enabled:
            await work(user)
        else:
            await sleep(user)


async def main(test: bool = False):
    """Start processor."""
    global _running
    if not _running:
        info("Starting main processor...")
        _ = signal.signal(signal.SIGINT, lambda _, __: stop())
        _ = signal.signal(signal.SIGTERM, lambda _, __: stop())
        _running = True
        if not test:
            async with asyncio.TaskGroup() as group:
                for user in _users:
                    debug("Creating task for user " + user.name)
                    task = group.create_task(_block(user))
                    _tasks_for_user.add(task)
                    task.add_done_callback(_tasks_for_user.discard)


async def exec_method_safe(method: str, *args: Any, **kwargs: Any) -> Any | None:
    """Execute method to gather infomation.

    Args:
        method(str): The method name, like get_list_apis, etc.
        *args(Any): arguments passed to method
        **kwargs(Any): keyword arguments passed to method
    Return:
        Any|None: execute result, None if any error happens
    """
    debug("Invoking method %s with args %s and kwargs %s", method, args, kwargs)
    task = asyncio.create_task(invoke(method, *args, **kwargs))
    _tasks_for_method.add(task)
    task.add_done_callback(_tasks_for_method.discard)
    return await task


def setup(*users: User):
    """Setup processor for users.

    Args:
        *users(User): The users to set
    """
    for user in users:
        if user not in _users:
            _users.append(user)


def stop():
    """Stop the processor."""
    global _running
    if _running:
        info("Stopping processor...")
        for task in _tasks_for_user:
            _ = task.cancel()
        _running = False


__all__ = ["call_next_api", "exec_method_safe", "get_list_apis", "main", "setup", "stop"]
