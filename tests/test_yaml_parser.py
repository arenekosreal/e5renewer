"""Test if YamlParser works."""

from yaml import dump
from pathlib import Path
from e5renewer.config import YamlParser


def test_yaml_parser(tmp_path: str):
    """Check if YamlParser correct."""
    yaml_path = Path(tmp_path) / "test.yaml"
    yaml_path2 = Path(tmp_path) / "test.yml"
    yaml_dict = {"test": "test"}
    assert YamlParser.test(yaml_path)
    assert YamlParser.test(yaml_path2)
    assert not YamlParser.test(Path("invalid.yam1"))
    with yaml_path.open("w", encoding="utf-8") as writer:
        dump(yaml_dict, writer)
    assert YamlParser.to_json(yaml_path) == yaml_dict
