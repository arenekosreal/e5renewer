from typing import ClassVar
from dataclasses import dataclass
from e5renewer.config import User
from e5renewer.logger import debug
from e5renewer.processor.statistic._method import register


@dataclass
class UsersStatus:
    """Storaging users status."""

    running: ClassVar[set[User]] = set()
    waiting: ClassVar[set[User]] = set()


_users_status = UsersStatus()
_results: dict[str, dict[str, list[str]]] = {}


def set_user_running(user: User, running: bool):
    if running:
        if user in _users_status.waiting:
            _users_status.waiting.discard(user)
        _users_status.running.add(user)
    else:
        if user in _users_status.running:
            _users_status.running.discard(user)
        _users_status.waiting.add(user)


def set_api_call_result(name: str, api_name: str, result: str):
    debug("Updating call result with user %s, api %s and result %s...", name, api_name, result)
    if name not in _results:
        _results[name] = {api_name: [result]}
    elif api_name not in _results[name]:
        _results[name][api_name] = [result]
    else:
        _results[name][api_name].append(result)


@register
async def get_running_users() -> list[str]:
    return [user.name for user in _users_status.running]


@register
async def get_waiting_users() -> list[str]:
    return [user.name for user in _users_status.waiting]


@register
async def get_user_results(user: str, api_name: str) -> list[str]:
    return _results.get(user, {}).get(api_name, [])
