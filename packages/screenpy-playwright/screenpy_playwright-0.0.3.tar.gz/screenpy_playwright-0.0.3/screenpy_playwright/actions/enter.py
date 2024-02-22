"""Enter text into an input field."""

from __future__ import annotations

from typing import TYPE_CHECKING

from screenpy.exceptions import UnableToAct
from screenpy.pacing import beat

if TYPE_CHECKING:
    from screenpy import Actor

    from ..target import Target


class Enter:
    """Enter text into an input field.

    Abilities Required:
        :class:`~screenpy_playwright.abilities.BrowseTheWebSynchronously`

    Examples::

        the_actor.attempts_to(Enter("Hello!").into_the(GREETING_INPUT))

        the_actor.attempts_to(Enter.the_text("eggs").into_the(GROCERY_FIELD))

        the_actor.attempts_to(Enter.the_secret("12345").into_the(PASSWORD_FIELD))
    """

    target: Target | None

    @staticmethod
    def the_text(text: str) -> Enter:
        """Provide the text to enter into the field.

        Args:
            text: the text to enter into the field.

        Returns:
            A new instance of Enter, with mask et to False.
        """
        return Enter(text)

    @staticmethod
    def the_secret(text: str) -> Enter:
        """Provide the SECRET text to enter into the field.

        The text will be masked, and appear as "[CENSORED]".

        Returns:
            A new instance of Enter, with mask set to True.
        """
        return Enter(text, mask=True)

    the_password = the_secret

    def into_the(self, target: Target) -> Enter:
        """Target the element to enter text into.

        Args:
            target: the Target which describes the element to enter text into.

        Returns:
            self
        """
        self.target = target
        return self

    into = into_the

    def describe(self) -> str:
        """Describe the Action in present tense.

        Returns:
            A description of this Action.
        """
        return f'Enter "{self.text_to_log}" into the {self.target}.'

    @beat('{} enters "{text_to_log}" into the {target}.')
    def perform_as(self, the_actor: Actor) -> None:
        """Direct the Actor to enter text into the Target."""
        if self.target is None:
            msg = (
                "Target was not supplied for Enter. Provide a Target by using either "
                "the .into(), .into_the(), or into_the_first_of_the() method."
            )
            raise UnableToAct(msg)

        self.target.found_by(the_actor).fill(self.text)

    def __init__(self, text: str, *, mask: bool = False) -> None:
        self.text = text
        self.target = None

        if mask:
            self.text_to_log = "[CENSORED]"
        else:
            self.text_to_log = text
