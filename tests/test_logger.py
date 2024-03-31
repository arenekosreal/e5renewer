"""Test if logger works."""

import logging
import e5renewer.logger
from e5renewer.logger import info
from e5renewer.logger import debug
from e5renewer.logger import error
from e5renewer.logger import _logger  # pyright: ignore
from e5renewer.logger import warning
from e5renewer.logger import setup_logger


def test_setup_logger():
    """Check if setup_logger is correct."""
    setattr(e5renewer.logger, "_is_set", False)
    setup_logger(True)
    assert _logger.level == logging.DEBUG
    setattr(e5renewer.logger, "_is_set", False)
    setup_logger(False)
    assert _logger.level == logging.INFO


def test_warning():
    """Check if warning is correct."""
    warning("Test warning message.")


def test_info():
    """Check if info is correct."""
    info("Test info message.")


def test_debug():
    """Check if debug is correct."""
    debug("Test debug message.")


def test_error():
    """Check if error is correct."""
    error("Test error message.")
