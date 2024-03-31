"""Logger module of E5Renewer."""

import inspect
import logging
from typing import Any
from e5renewer.defines import NAME


_logger = logging.getLogger(NAME)
_is_set = False


def error(msg: str, *args: Any):
    """Create an error message.

    Args:
        msg(str): The message or message format string
        *args(Any): Any objects applied to `msg`
    """
    if _is_set:
        frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(frame, 2)[1]
        module = inspect.getmodule(caller_frame.frame)
        header = (module.__name__ + "." if module else "") + caller_frame.function + ": "
        _logger.error(header + msg, *args)


def warning(msg: str, *args: Any):
    """Create a warning message.

    Args:
        msg(str): The message or message format string
        *args(Any): Any objects applied to `msg`
    """
    if _is_set:
        frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(frame, 2)[1]
        module = inspect.getmodule(caller_frame.frame)
        header = (module.__name__ + "." if module else "") + caller_frame.function + ": "
        _logger.warning(header + msg, *args)


def info(msg: str, *args: Any):
    """Create an info message.

    Args:
        msg(str): The message or message format string
        *args(Any): Any objects applied to `msg`
    """
    if _is_set:
        frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(frame, 2)[1]
        module = inspect.getmodule(caller_frame.frame)
        header = (module.__name__ + "." if module else "") + caller_frame.function + ": "
        _logger.info(header + msg, *args)


def debug(msg: str, *args: Any):
    """Create a debug message.

    Args:
        msg(str): The message or message format string
        *args(Any): Any objects applied to `msg`
    """
    if _is_set:
        frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(frame, 2)[1]
        module = inspect.getmodule(caller_frame.frame)
        header = (module.__name__ + "." if module else "") + caller_frame.function + ": "
        _logger.debug(header + msg, *args)


def setup_logger(debug: bool):
    """Setup logger.

    Args:
        debug(bool): If set logging level to debug
    """
    global _is_set
    if not _is_set:
        _logger.setLevel(logging.DEBUG if debug else logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s-%(levelname)s-%(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            ),
        )
        _logger.addHandler(handler)
        _is_set = True
