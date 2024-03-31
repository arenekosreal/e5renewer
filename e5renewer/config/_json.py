import json
from typing import Any
from pathlib import Path
from e5renewer.defines import AUTHOR
from typing_extensions import override
from e5renewer.config._parser import ConfigParser
from e5renewer.config._parser import config_parser


@config_parser
class JsonParser(ConfigParser):
    @property
    @override
    def name(self) -> str:
        return "Json Config Parser"

    @property
    @override
    def author(self) -> str:
        return AUTHOR

    @classmethod
    @override
    def to_json(cls, path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as reader:
            return json.load(reader)

    @classmethod
    @override
    def test(cls, path: Path) -> bool:
        return path.name.endswith(".json")
