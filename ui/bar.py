"""Progress / health bar UI element with support for dynamic (callable) values."""

import pygame

from .ui_element import UIElement


class Bar(UIElement):
    """Horizontal bar. value and max_value can be numbers or callables."""

    def __init__(
        self,
        value,
        max_value=100,
        width=180,
        height=20,
        fill_color=(220, 60, 60),
        bg_color=(45, 25, 30),
        border_color=(90, 90, 120),
        border_width=2,
    ):
        super().__init__(width=width, height=height)
        self._value = value
        self._max_value = max_value
        self.fill_color = fill_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width

    def _get_value(self):
        return self._value() if callable(self._value) else self._value

    def _get_max_value(self):
        return self._max_value() if callable(self._max_value) else self._max_value

    def draw(self, screen):
        if not self.visible:
            return

        ax, ay = self.get_absolute_position()
        bg_rect = pygame.Rect(ax, ay, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, bg_rect)

        max_val = self._get_max_value()
        val = self._get_value()
        ratio = max(0.0, min(1.0, val / max_val)) if max_val > 0 else 0.0

        fill_width = round(self.width * ratio)
        if fill_width > 0:
            fill_rect = pygame.Rect(ax, ay, fill_width, self.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect)

        if self.border_width > 0 and self.border_color is not None:
            pygame.draw.rect(screen, self.border_color, bg_rect, self.border_width)
