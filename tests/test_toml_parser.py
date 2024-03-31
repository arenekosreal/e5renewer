"""Test if TomlParser works."""

from pathlib import Path
from tomli_w import dump
from e5renewer.config import TomlParser


def test_toml_parser(tmp_path: str):
    """Check if TomlParser correct."""
    toml_path = Path(tmp_path) / "test.toml"
    toml_dict = {"test": "test"}
    assert TomlParser.test(toml_path)
    assert not TomlParser.test(Path("invalid.t0m1"))
    with toml_path.open("wb") as writer:
        dump(toml_dict, writer)
    assert TomlParser.to_json(toml_path) == toml_dict
