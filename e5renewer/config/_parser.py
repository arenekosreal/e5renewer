from abc import abstractmethod
from typing import Any
from pathlib import Path
from e5renewer.sdk import Module
from e5renewer.sdk import module


class ConfigParser(Module):
    @classmethod
    @abstractmethod
    def to_json(cls, path: Path) -> dict[str, Any]: ...

    @classmethod
    @abstractmethod
    def test(cls, path: Path) -> bool: ...


_known_parsers: set[type[ConfigParser]] = set()


def config_parser(parser: type[ConfigParser]) -> type[ConfigParser]:
    """Register class is a ConfigParser."""
    if parser not in _known_parsers:
        parser = module()(parser)
        _known_parsers.add(parser)
    return parser


def get_parser(path: Path) -> type[ConfigParser] | None:
    """Get config parser which can parse config file given.

    Args:
        path(Path): the path of a config

    Returns:
        type[ConfigParser] | None ConfigParser type if found, None else.
    """
    results = [parser for parser in _known_parsers if parser.test(path)]
    return results[0] if len(results) > 0 else None
