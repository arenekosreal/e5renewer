"""Test if Module works."""

from e5renewer.sdk import Module
from e5renewer.sdk import SemVer
from e5renewer.sdk import module
from typing_extensions import override
from e5renewer.sdk._module import _MODULE_API_VERSION  # pyright: ignore


def test_module_changed():
    """Check if module with version overriden is correct."""

    @module(SemVer(0, 0, 0))
    class DummyModule(Module):
        @property
        @override
        def name(self) -> str:
            return "DummyModule"

        @property
        @override
        def author(self) -> str:
            return "Pytest"

    m = DummyModule()
    assert m.api_version == SemVer(0, 0, 0)
    assert m.name == "DummyModule"
    assert m.author == "Pytest"
    assert m.is_deprecated


def test_module():
    """Check if module correct."""

    class DummyModule(Module):
        @property
        @override
        def name(self) -> str:
            return "DummyModule"

        @property
        @override
        def author(self) -> str:
            return "Pytest"

    m = DummyModule()
    assert m.api_version == _MODULE_API_VERSION
    assert not m.is_deprecated
