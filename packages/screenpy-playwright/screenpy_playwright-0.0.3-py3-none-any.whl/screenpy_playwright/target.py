"""Represent an element on the page using its locator and a description."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .abilities import BrowseTheWebSynchronously
from .exceptions import TargetingError

if TYPE_CHECKING:
    from playwright.sync_api import FrameLocator, Locator, Page
    from screenpy import Actor
    from typing_extensions import Self


class Target:
    """A described element on a webpage.

    Examples::

        Target.the('"Log In" button').located_by("button:has-text('Log In')")

        Target.the("toast message").located_by("//toast")

        Target.the('"Pick up Milk" todo item").located_by(
            "_vue=list-item[text *= 'milk' i]"
        )

        Target().located_by("#enter-todo-field")
    """

    locator: str | None
    frame_path: list[str]
    _description: str | None

    @classmethod
    def the(cls: type[Self], name: str) -> Self:
        """Provide a human-readable description of the target."""
        return cls(name)

    def located_by(self, locator: str) -> Target:
        """Provide the Playwright locator which describes the element."""
        self.locator = locator
        return self

    def in_frame(self, frame_locator: str) -> Target:
        """Provide the Playwright locator which describes the frame."""
        self.frame_path.append(frame_locator)
        return self

    @property
    def target_name(self) -> str:
        """Get the name of the Target.

        Returns:
            The text representation of this Target.
        """
        return self._description or self.locator or "None"

    @target_name.setter
    def target_name(self, value: str) -> None:
        """Set the target_name.

        Args:
            value: the new description to use.
        """
        self._description = value

    def found_by(self, the_actor: Actor) -> Locator:
        """Get the Playwright Locator described by this Target.

        Args:
            the_actor: the Actor who should find this Locator.

        Returns:
            The Locator which describes the element.
        """
        browse_the_web = the_actor.ability_to(BrowseTheWebSynchronously)
        if browse_the_web.current_page is None:
            msg = f"There is no active page! {the_actor} cannot find the {self}."
            raise TargetingError(msg)
        if self.locator is None:
            msg = f"{self} does not have a locator set."
            raise TargetingError(msg)

        frame: Page | FrameLocator = browse_the_web.current_page
        for frame_locator in self.frame_path:
            frame = frame.frame_locator(frame_locator)

        return frame.locator(self.locator)

    def __repr__(self) -> str:
        """Get a human-readable representation of this Target.

        Returns:
            A string representing this Target.
        """
        return self.target_name

    def __init__(self, name: str | None = None) -> None:
        self._description = name
        self.locator = None
        self.frame_path = []
