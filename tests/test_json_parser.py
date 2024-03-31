"""Test if JsonParser class works."""

from json import dump
from pathlib import Path
from e5renewer.config import JsonParser


def test_json_parser(tmp_path: str):
    """Check if JsonParser correct."""
    json_path = Path(tmp_path) / "test.json"
    json_dict = {"test": "test"}
    assert JsonParser.test(json_path)
    assert not JsonParser.test(Path("invalid-json.js0n"))
    with json_path.open("w", encoding="utf-8") as writer:
        dump(json_dict, writer)
    assert JsonParser.to_json(json_path) == json_dict
