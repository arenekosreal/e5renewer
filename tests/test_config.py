"""Test config deserialization functions."""

import pytest
import socket
from typing import Any
from typing import Self
from pathlib import Path
from datetime import time
from e5renewer.config import User
from e5renewer.config import Config
from typing_extensions import override
from e5renewer.config._base import BaseConfig


def test_baseconfig_init():
    """Check if BaseConfig is correct."""

    class DummyBaseConfig(BaseConfig):
        @classmethod
        @override
        def from_json(cls, json: dict[str, Any]) -> Self:
            return cls.__new__(cls)

        @property
        @override
        def is_valid(self) -> bool:
            return True

    with pytest.raises(RuntimeError):
        _ = DummyBaseConfig()


def test_user(secret: str):
    """Check if User is correct."""
    json = {
        "name": "me@test.com",
        "client_id": "test-client-id",
        "secret": secret,
        "tenant_id": "test-tenant",
        "from_time": "00:00:00",
        "to_time": "00:00:00",
    }
    target = User.__new__(User)
    target.name = "me@test.com"
    target.client_id = "test-client-id"
    target.secret = secret
    target.tenant_id = "test-tenant"
    instance = User.from_json(json)
    assert instance.is_valid
    assert instance == target


def test_config(secret: str, unused_tcp_port: int):
    """Check if Config is correct."""
    json = {
        "auth_token": secret,
        "listen_addr": "127.0.0.1",
        "listen_port": unused_tcp_port,
        "users": [
            {
                "name": "me@test.com",
                "client_id": "test-client-id",
                "secret": secret,
                "tenant_id": "test-tenant",
                "from_time": "00:00:00",
                "to_time": "00:00:00",
            },
        ],
    }
    target = Config.__new__(Config)
    target.auth_token = secret
    target.listen_addr = "127.0.0.1"
    target.listen_port = unused_tcp_port
    user = User.__new__(User)
    user.name = "me@test.com"
    user.client_id = "test-client-id"
    user.secret = secret
    user.tenant_id = "test-tenant"
    user.from_time = time()
    user.to_time = time()
    setattr(target, "users", [user])
    instance = Config.from_json(json)
    assert instance.is_valid
    assert instance == target


def test_config_is_listen_valid_http():
    """Check if _is_listen_valid with http correct."""
    instance = Config.__new__(Config)
    instance.listen_addr = "127.0.0.1"
    instance.listen_port = 80
    assert instance._is_listen_valid  # pyright: ignore[reportPrivateUsage]


@pytest.mark.skipif(not hasattr(socket, "AF_UNIX"), reason="Unix socket is unsupported on windows")
def test_config_is_listen_valid_socket(tmp_path: str):
    """Check if _is_listen_valid with socket correct."""
    instance = Config.__new__(Config)
    instance.listen_socket = Path(tmp_path) / "e5renewer.socket"
    instance.listen_socket_permission = 666
    assert instance._is_listen_valid  # pyright: ignore[reportPrivateUsage]


def test_config_is_valid_http(secret: str):
    """Check if is_valid with http correct."""
    instance = Config.__new__(Config)
    instance.listen_addr = "127.0.0.1"
    instance.listen_port = 80
    instance.auth_token = secret
    assert instance.is_valid


@pytest.mark.skipif(not hasattr(socket, "AF_UNIX"), reason="Unix socket is unsupported on windows")
def test_config_is_valid_socket(tmp_path: str, secret: str):
    """Check if is_valid with socket correct."""
    instance = Config.__new__(Config)
    instance.listen_socket = Path(tmp_path) / "e5renewer.socket"
    instance.listen_socket_permission = 666
    instance.auth_token = secret
    assert instance.is_valid
