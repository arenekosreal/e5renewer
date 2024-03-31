"""Test if SemVer works."""

from e5renewer.sdk import SemVer


def test_semver_eq():
    """Check if SemVer equals to SemVer is correct."""
    assert SemVer(0, 1, 0) == SemVer(0, 1, 0)
    assert SemVer(0, 1, 0) is not None


def test_semver_lt():
    """Check if SemVer less than SemVer is correct."""
    assert SemVer(0, 1, 0) < SemVer(0, 2, 0)


def test_semver_gt():
    """Check if SemVer greater than SemVer is correct."""
    assert SemVer(0, 4, 0) > SemVer(0, 0, 0)


def test_semver_str():
    """Check if SemVer to string is correct."""
    assert str(SemVer(0, 1, 0)) == "0.1.0"
