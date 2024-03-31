"""Network module for E5Renewer."""

import time
import socket
import asyncio
from typing import Any
from typing import Callable
from typing import Awaitable
from aiohttp import web
from pathlib import Path
from e5renewer.logger import info
from e5renewer.processor import main as processor_start
from e5renewer.processor import stop as processor_stop
from e5renewer.processor import exec_method_safe
from e5renewer.network._auth import check_auth
from e5renewer.network._auth import setup_auth
from e5renewer.network._auth import check_outdate


_routes = web.RouteTableDef()


def octal_to_decimal(value: int) -> int:
    octal_int = 0
    dights = [int(i) for i in str(value)]
    for i in range(len(dights)):
        octal_int += dights[i] * pow(8, len(dights) - i - 1)
    return octal_int


async def processor_controls(app: web.Application):
    info("Starting processor...")
    processor = web.AppKey("processor", asyncio.Task[None])
    app[processor] = asyncio.create_task(processor_start())

    yield

    _ = app[processor].cancel()
    await app[processor]


@web.middleware
async def permission_check(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:
    authentication = request.headers.get("Authentication")
    if authentication and check_auth(authentication):
        return await handler(request)
    raise web.HTTPForbidden(text="Authenticate failed")


@web.middleware
async def timestamp_check(
    request: web.Request,
    handler: Callable[[web.Request], Awaitable[web.StreamResponse]],
) -> web.StreamResponse:
    match request.method:
        case "GET":
            try:
                timestamp = int(request.query.get("timestamp", "-1"))
            except Exception:
                timestamp = -1
            if check_outdate(timestamp):
                return await handler(request)
            raise web.HTTPForbidden(text="Request is outdated")
        case "POST":
            try:
                body = await request.json()
                if not isinstance(body, dict):
                    raise ValueError("Invalid body %s", body)
            except Exception as exc:
                raise web.HTTPBadRequest from exc
            else:
                try:
                    timestamp = int(
                        body.get("timestamp", "-1"),  # type: ignore
                    )
                except Exception:
                    timestamp = -1
                if check_outdate(timestamp):
                    return await handler(request)
                raise web.HTTPForbidden(text="Request is outdated")
        case _:
            raise web.HTTPBadRequest


@_routes.get("/v1/{name}")
async def get_infomation(request: web.Request) -> web.Response:
    name = request.match_info.get("name", "")
    if "/" in name or len(name) == 0:
        raise web.HTTPBadRequest(text="Invalid method {method}".format(method=name))
    args = dict(request.query)
    _ = args.pop("timestamp", None)
    data: dict[str, Any] = {
        "method": name,
        "args": args,
        "result": await exec_method_safe(request.method.lower() + "_" + name, **args),
        "timestamp": int(time.time() * 1000),
    }
    return web.json_response(data)


def main(
    listen_addr: str | None,
    listen_port: int | None,
    listen_socket: Path | None,
    lisen_socket_permission: int | None,
    dry_run: bool = False,
):
    """Start network module.

    We will use listen_addr and listen_port to create TCP socket,
    create unix domain socket when listen_addr or listen_port
    is not set and your platform supports unix domain socket.

    Args:
        listen_addr(str|None): Bind address
        listen_port(int|None): Bind port
        listen_socket(Path|None): Bind unix domain socket
        lisen_socket_permission(int|None): Permission of unix domain socket
        dry_run(bool): If do not perform actual job, defaults to False
    Raises:
        RuntimeError: When listen_addr and listen_port is not set and unix domain socket
                      is not set or supported
    """

    async def on_startup(_: web.Application):
        if listen_socket and listen_socket.parent.exists() and lisen_socket_permission:
            listen_socket.chmod(octal_to_decimal(lisen_socket_permission))

    async def close_processor(_: web.Application):
        processor_stop()

    info("Starting network server...")

    app = web.Application(middlewares=[timestamp_check, permission_check])
    app.on_startup.append(on_startup)
    app.on_cleanup.append(close_processor)
    app.cleanup_ctx.append(processor_controls)
    _ = app.add_routes(_routes)
    if listen_addr and listen_port:
        listen_string = "http://%s:%d" % (listen_addr, listen_port)
        args = {"host": listen_addr, "port": listen_port}
    elif listen_socket and hasattr(socket, "AF_UNIX"):
        listen_string = "unix:/%s" % listen_socket.as_posix()
        args = {"path": listen_socket}
    else:
        raise RuntimeError("Failed to start server")
    info("Listening on %s" % listen_string)
    if not dry_run:
        web.run_app(app, **args)  # type: ignore


__all__ = ["main", "setup_auth"]
