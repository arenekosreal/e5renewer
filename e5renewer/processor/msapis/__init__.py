"""Classes and utils for invoking msgraph apis."""

import random
from e5renewer.config import User
from e5renewer.logger import info
from e5renewer.processor.msapis._get import *
from e5renewer.processor.msapis._caller import APICaller
from e5renewer.processor.msapis._caller import get_list_apis
from e5renewer.processor.msapis._random import RandomAPICaller


_callers: dict[User, APICaller] = {}


async def call_next_api(user: User):
    """Call next api for user.

    We will choice an api caller randomly if user does not have its caller.

    Args:
        user(User): The user to call api
    """
    if user not in _callers:
        _callers[user] = random.choice([RandomAPICaller])(user)
    info("Calling API by using %s for user %s", _callers[user].__class__.__name__, user.name)
    await _callers[user].call_next_api()


__all__ = ["call_next_api", "get_list_apis"]
