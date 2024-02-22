"""Exceptions thrown by ScreenPy: Playwright."""

from screenpy.exceptions import ScreenPyError


class TargetingError(ScreenPyError):
    """There was an issue targeting an element."""
