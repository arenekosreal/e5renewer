"""Test if ConfigParser class works."""

from typing import Any
from pathlib import Path
from typing_extensions import override
from e5renewer.config._parser import ConfigParser
from e5renewer.config._parser import config_parser


class DummyConfigParser(ConfigParser):
    """Dummy test class for ConfigParser."""

    @property
    @override
    def name(self) -> str:
        return "Test"

    @property
    @override
    def author(self) -> str:
        return "Test"

    @classmethod
    @override
    def to_json(cls, path: Path) -> dict[str, Any]:
        return {"test": True}


def test_config_parser():
    """Check if config_parser can register class."""
    assert config_parser(DummyConfigParser) == DummyConfigParser
