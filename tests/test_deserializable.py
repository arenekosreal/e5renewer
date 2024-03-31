"""Test if DeserializableObject class works."""

from typing import Any
from typing import Self
from e5renewer.defines import DeserializableObject
from typing_extensions import override


class DeserializableObjectForTest(DeserializableObject):
    """Dummy test class for DeserializableObject."""

    @classmethod
    @override
    def from_json(cls, json: dict[str, Any]) -> Self:
        return cls.__new__(cls)

    @property
    @override
    def is_valid(self) -> bool:
        return True


def test_deserializable_eq():
    """Check if DeserializableObject.__eq__() is correct."""
    obja = DeserializableObjectForTest.__new__(DeserializableObjectForTest)
    objb = DeserializableObjectForTest.__new__(DeserializableObjectForTest)
    assert obja.__eq__(objb)
