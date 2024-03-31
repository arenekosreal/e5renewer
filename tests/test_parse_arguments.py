"""Test if _parse_arguments works."""

import sys
from pathlib import Path
from e5renewer import _parse_arguments  # pyright: ignore[reportPrivateUsage]


def test_parse_arguments(tmp_path: str):
    """Check if _parse_arguments correct."""
    json_path = Path(tmp_path) / "config.json"
    argv = sys.argv
    sys.argv = [sys.argv[0], "--config", str(json_path.absolute()), "--test"]
    assert _parse_arguments().config == str(json_path.absolute())
    assert sys.argv == ["--test"]
    sys.argv = argv
