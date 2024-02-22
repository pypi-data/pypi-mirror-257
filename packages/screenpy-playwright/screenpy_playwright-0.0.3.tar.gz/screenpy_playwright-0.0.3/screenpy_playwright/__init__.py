"""
                              ScreenPy Playwright.

                                                                      FADE IN:

INT. SITEPACKAGES DIRECTORY

ScreenPy Playwright is an extension for ScreenPy which enables Actors to use
the Playwright browser automation tool.

:copyright: (c) 2019-2024 by Perry Goy.
:license: MIT, see LICENSE for more details.
"""

from . import abilities, actions, questions
from .abilities import *  # noqa: F403
from .actions import *  # noqa: F403
from .exceptions import TargetingError
from .protocols import PageObject
from .questions import *  # noqa: F403
from .target import Target

__all__ = ["Target", "TargetingError", "PageObject"]

__all__ += abilities.__all__ + actions.__all__ + questions.__all__
