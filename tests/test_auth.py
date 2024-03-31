"""Test if authentication helpers are correct."""

import time
from e5renewer.network import check_auth
from e5renewer.network import setup_auth
from e5renewer.network import check_outdate


def test_setup_auth():
    """Check if setup_auth is correct."""
    setup_auth("test-auth-token")


def test_check_auth():
    """Check if check_auth is correct."""
    setup_auth("test-auth-token")
    assert not check_auth("test-auth")
    assert check_auth("test-auth-token")


def test_check_outdate():
    """Check if check_outdate is correct."""
    timestamp = int((time.time() - 1) * 1000)
    assert check_outdate(timestamp)
