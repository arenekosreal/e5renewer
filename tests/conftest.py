"""Fixtures used in tests."""

import time
import uuid
import pytest
import random
import string
from e5renewer.config import User


@pytest.fixture()
def secret() -> str:
    """Generate a random string in 64 characters.

    Returns:
        str: The random string
    """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(64))


@pytest.fixture()
def user(secret: str) -> User:
    """Generate a random User instance.

    Args:
        secret(str): Generated random string as secret in User

    Returns:
        User: The User instance
    """
    return User.from_json(
        {
            "name": "pytest",
            "tenant_id": str(uuid.uuid4()),
            "client_id": str(uuid.uuid4()),
            "secret": secret,
            "from_time": "00:00:00",
            "to_time": "23:59:59",
        },
    )


@pytest.fixture()
def timestamp() -> int:
    """Generate a timestamp for request/response.

    Returns:
        int: The timestamp
    """
    return int(time.time() * 1000)
