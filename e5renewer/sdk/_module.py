from abc import ABC
from abc import abstractmethod
from typing import TypeVar
from typing import Callable
from e5renewer.sdk._semver import SemVer


_MODULE_API_VERSION = SemVer(0, 1, 0)


class Module(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Module name."""
        ...

    @property
    @abstractmethod
    def author(self) -> str:
        """Module author."""
        ...

    @property
    def api_version(self) -> SemVer:
        """Module API version."""
        return _MODULE_API_VERSION

    @property
    def is_deprecated(self) -> bool:
        return self.api_version != _MODULE_API_VERSION


_known_modules: set[type[Module]] = set()
_T = TypeVar("_T", bound="Module")


def module(version: SemVer = _MODULE_API_VERSION) -> Callable[[type[_T]], type[_T]]:
    """Register class is module.

    Using as decorator is prefered.

    Args:
        version(SemVer): override module api_version, defaults to SemVer(0, 1, 0)

    Returns:
        Callable[[type[Module]], type[Module]]: the function wrapper register the module
    """

    def _module(cls: type[_T]) -> type[_T]:
        if cls not in _known_modules:
            if version != _MODULE_API_VERSION:

                @property
                def _version(_: _T) -> SemVer:
                    return version

                setattr(cls, "api_version", _version)
            _known_modules.add(cls)
        return cls

    return _module
