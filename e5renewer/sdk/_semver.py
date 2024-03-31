from typing import NamedTuple
from typing_extensions import override


class SemVer(NamedTuple):
    """SemVer helps indicating compatibility level."""

    major: int
    minor: int
    patch: int

    @override
    def __str__(self) -> str:
        """major.minor.patch format in string."""
        return ".".join([str(self.major), str(self.minor), str(self.patch)])
