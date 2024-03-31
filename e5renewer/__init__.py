"""E5Renewer main module."""

import sys
import signal
from types import FrameType
from typing import Any
from typing import Self
from pathlib import Path
from argparse import ArgumentParser
from e5renewer.config import Config
from e5renewer.config import get_parser
from e5renewer.logger import debug
from e5renewer.logger import setup_logger
from e5renewer.defines import DeserializableObject
from e5renewer.network import main as network_start
from e5renewer.network import setup_auth
from typing_extensions import override
from e5renewer.processor import setup


class ArgumentParseResult(DeserializableObject):
    """Parsed result of arguments."""

    config = ""
    debug = False

    @classmethod
    @override
    def from_json(cls, json: dict[str, Any]) -> Self:
        instance = cls.__new__(cls)
        for key in dir(instance):
            if key in json:
                json_val = json[key]
                match key:
                    case "config" | "debug":
                        if isinstance(json_val, type(getattr(instance, key))):
                            setattr(instance, key, json_val)
                    case _:
                        pass
        if instance.is_valid:
            return instance
        raise RuntimeError("Failed to parse arguments")

    @property
    @override
    def is_valid(self) -> bool:
        return bool(self.config)


def _parse_arguments() -> ArgumentParseResult:
    parser = ArgumentParser()
    _ = parser.add_argument("--config", "-c", help="Config file path", required=True)
    _ = parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    namespace, sys.argv = parser.parse_known_args()
    return ArgumentParseResult.from_json({"config": namespace.config, "debug": namespace.debug})


def _on_sigterm_triggered(_: int, __: FrameType | None):
    sys.exit()


def main(test: bool = False):
    """The main entrance of E5Renewer."""
    arguments = _parse_arguments()
    config = Path(arguments.config).absolute()
    if not config.is_file():
        raise RuntimeError("The config path %s is not a file" % arguments.config)
    parser = get_parser(config)
    if not parser:
        raise RuntimeError("Unable to find parser for config %s" % arguments.config)
    json = parser.to_json(config)
    config_instance = Config.from_json(json if json else {})
    setup_logger(arguments.debug or config_instance.debug)
    setup(*config_instance.users)
    _ = signal.signal(signal.SIGTERM, _on_sigterm_triggered)
    debug("Setting up program...")
    if not test:
        setup_auth(config_instance.auth_token)
        network_start(
            config_instance.listen_addr,
            config_instance.listen_port,
            config_instance.listen_socket,
            config_instance.listen_socket_permission,
        )


__all__ = ["main"]
