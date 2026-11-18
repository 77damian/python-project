"""Text label UI element with support for dynamic (callable) text."""

from typing import Callable

import pygame

from .ui_element import UIElement


class Label(UIElement):
    """Text label. text can be a string or a callable that returns a string (auto-updates)."""

    def __init__(
        self,
        text: str | Callable[[], str],
        font_size: int = 20,
        color: tuple[int, int, int] = (255, 255, 255),
        align: str = "left",
    ) -> None:
        super().__init__()
        self._text: str | Callable[[], str] = text  # str or callable
        self.font_size: int = font_size
        self.color: tuple[int, int, int] = color
        self.align: str = align  # "left", "center", "right"
        self._font: pygame.font.Font = pygame.font.Font(None, font_size)
        self._update_size()

    @property
    def text(self) -> str:
        """Return the current text, calling the callable if needed."""
        if callable(self._text):
            return self._text()
        return self._text

    @text.setter
    def text(self, value: str | Callable[[], str]) -> None:
        """Set the text (string or callable) and recalculate size."""
        self._text = value
        self._update_size()

    def _update_size(self) -> None:
        """Recalculate width/height from the current rendered text."""
        rendered = self._font.render(self.text, True, self.color)
        self.width = rendered.get_width()
        self.height = rendered.get_height()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the label text at its absolute position."""
        if not self.visible:
            return
        text_surf = self._font.render(self.text, True, self.color)
        ax, ay = self.get_absolute_position()

        # Update size for dynamic text
        self.width = text_surf.get_width()
        self.height = text_surf.get_height()

        screen.blit(text_surf, (ax, ay))
