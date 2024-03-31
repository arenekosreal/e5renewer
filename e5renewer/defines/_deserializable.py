import json
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Self
from typing_extensions import override


class DeserializableObject(ABC):
    """A object which can be deserialized from a json dict."""

    _indent = 4

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict[str, Any]) -> Self:
        """Generate instance from json dict.

        Args:
            json (dict[str, Any]): input json

        Returns:
            DeserializableObject: instance
        """
        ...

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        """If the instance is valid."""
        ...

    @override
    def __eq__(self, __value: object) -> bool:
        if hasattr(__value, "__dict__"):
            return self.__dict__ == __value.__dict__
        return False

    @override
    def __str__(self) -> str:
        dict_to_return: dict[str, Any] = {}
        for key, item in self.__dict__.items():
            if key.startswith("_") or callable(item):
                continue
            dict_to_return[key] = item
        return json.dumps(dict_to_return, indent=self._indent, sort_keys=True)

    @override
    def __hash__(self) -> int:
        return hash(str(self))
