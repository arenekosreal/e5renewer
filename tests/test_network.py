"""Test if network utils works."""

import pytest
import socket
from http import HTTPStatus
from typing import Any
from typing import Callable
from typing import Awaitable
from typing import Coroutine
from asyncio import CancelledError
from asyncio import AbstractEventLoop
from pathlib import Path
from aiohttp.web import Request
from aiohttp.web import Response
from aiohttp.web import Application
from aiohttp.web import HTTPForbidden
from aiohttp.web import HTTPBadRequest
from aiohttp.web import StreamResponse
from e5renewer.network import main
from e5renewer.network import setup_auth
from e5renewer.network import get_infomation
from e5renewer.network import timestamp_check
from e5renewer.network import octal_to_decimal
from e5renewer.network import permission_check
from e5renewer.network import processor_controls
from aiohttp.test_utils import TestClient
from aiohttp.test_utils import make_mocked_request


TARGET_OCTAL_NUM = 0o777
SOURCE_OCTAL_NUM = 777
AioHTTPClientType = Callable[[Application], Coroutine[Any, Any, TestClient]]
RequestHandlerType = Callable[[Request], Awaitable[StreamResponse]]


def test_octal_to_decimal():
    """Check if converting octal to dights is correct."""
    assert octal_to_decimal(SOURCE_OCTAL_NUM) == TARGET_OCTAL_NUM


@pytest.mark.asyncio()
async def test_processor_controls():
    """Check if processor_controls is correct."""
    app = Application()
    gen = processor_controls(app)
    await anext(gen)
    with pytest.raises(CancelledError):
        await anext(gen)


@pytest.fixture()
def dummy_handler() -> RequestHandlerType:
    """Generate a dummy handler for handling web request.

    Returns:
        RequestHandlerType: The handler function
    """

    async def handler(_: Request) -> StreamResponse:
        return Response()

    return handler


@pytest.fixture()
def empty_get_request() -> Request:
    """Generate a GET Request without anything.

    Returns:
        Request: The request instance.
    """
    return make_mocked_request("GET", "/v1/test")


@pytest.fixture()
def empty_post_request() -> Request:
    """Generate a POST Request without anything.

    Returns:
        Request: The request instance.
    """
    return make_mocked_request("POST", "/v1/test")


@pytest.fixture()
def empty_put_request() -> Request:
    """Generate a PUT Request without anything.

    Returns:
        Request: The request instance.
    """
    return make_mocked_request("PUT", "/v1/test")


@pytest.mark.asyncio()
async def test_permission_check_no_auth(
    empty_get_request: Request,
    dummy_handler: RequestHandlerType,
    secret: str,
):
    """Check if permission_check is correct when no authentication is set."""
    setup_auth(secret)
    with pytest.raises(HTTPForbidden):
        _ = await permission_check(empty_get_request, dummy_handler)


@pytest.mark.asyncio()
async def test_timestamp_check_get(
    empty_get_request: Request,
    dummy_handler: RequestHandlerType,
):
    """Check if timestamp_check is correct when is GET request."""
    with pytest.raises(HTTPForbidden):
        _ = await timestamp_check(empty_get_request, dummy_handler)


@pytest.mark.asyncio()
async def test_timestamp_check_post(
    empty_post_request: Request,
    dummy_handler: RequestHandlerType,
):
    """Check if timestamp_check is correct when is POST request."""
    with pytest.raises(HTTPBadRequest):
        _ = await timestamp_check(empty_post_request, dummy_handler)


@pytest.mark.asyncio()
async def test_timestamp_check_put(
    empty_put_request: Request,
    dummy_handler: RequestHandlerType,
):
    """Check if timestamp_check is correct when is PUT request."""
    with pytest.raises(HTTPBadRequest):
        _ = await timestamp_check(empty_put_request, dummy_handler)


@pytest.fixture()
def http_client(event_loop: AbstractEventLoop, aiohttp_client: AioHTTPClientType) -> TestClient:
    """Generate a TestClient for server testing.

    Args:
        event_loop(AbstractEventLoop): `event_loop` fixture by pytest-aiohttp
        aiohttp_client(AioHTTPClientType): `aiohttp_client` fixture by pytest-aiohttp

    Returns:
        TestClient: The TestClient instance
    """
    app = Application(middlewares=[timestamp_check, permission_check])
    _ = app.router.add_get("/v1/{name}", get_infomation)
    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.mark.asyncio()
async def test_http_server_no_authentication(http_client: TestClient):
    """Check if http server is correct when no authentication in headers."""
    resp = await http_client.get("/v1/test")
    assert resp.status == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio()
async def test_http_server_no_timestamp(http_client: TestClient, secret: str):
    """Check if http server is correct when no timestamp in query params."""
    setup_auth(secret)
    resp = await http_client.get(
        "/v1/test",
        headers={"Authentication": secret},
    )
    assert resp.status == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio()
async def test_http_server_ok(http_client: TestClient, secret: str, timestamp: int):
    """Check if http server is correct when request has authentication and timestamp."""
    setup_auth(secret)
    resp = await http_client.get(
        "/v1/test",
        headers={"Authentication": secret},
        params={"timestamp": str(timestamp)},
    )
    assert resp.status == HTTPStatus.OK


@pytest.mark.asyncio()
async def test_http_server_not_found(http_client: TestClient, secret: str, timestamp: int):
    """Check if http server is correct when requested an invalid path."""
    setup_auth(secret)
    resp = await http_client.get(
        "/v1",
        headers={"Authentication": secret},
        params={"timestamp": str(timestamp)},
    )
    assert resp.status == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio()
async def test_http_server_outdated(http_client: TestClient, secret: str, timestamp: int):
    """Check if http server is correct when timestamp is outdated."""
    timestamp += 30 * 1000  # Force it outdate
    setup_auth(secret)
    resp = await http_client.get(
        "/v1/test",
        headers={"Authentication": secret},
        params={"timestamp": str(timestamp)},
    )
    assert resp.status == HTTPStatus.FORBIDDEN


def test_main_tcp(unused_tcp_port: int):
    """Check if main is correct when listening tcp socket."""
    main("127.0.0.1", unused_tcp_port, None, None, True)


@pytest.mark.skipif(
    not hasattr(socket, "AF_UNIX"),
    reason="Unix socket is not available on this platform.",
)
def test_main_socket(tmp_path: str):
    """Check if main is correct when listening unix socket."""
    main(None, None, Path(tmp_path) / "temp.socket", 644, True)


def test_main_listen_failed():
    """Check if main is correct when everything is None."""
    with pytest.raises(RuntimeError):
        main(None, None, None, None, True)
