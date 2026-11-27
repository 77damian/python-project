"""Clickable button UI element with hover/press states."""

from typing import Callable

import pygame

from .ui_element import UIElement


class Button(UIElement):
    """Clickable button with text, hover/press states."""

    NORMAL: int = 0
    HOVER: int = 1
    PRESSED: int = 2

    def __init__(
        self,
        text: str | Callable[[], str],
        width: int = 150,
        height: int = 40,
        on_click: Callable[[], None] | None = None,
        bg_color: tuple[int, int, int] = (60, 60, 60),
        hover_color: tuple[int, int, int] = (80, 80, 80),
        press_color: tuple[int, int, int] = (40, 40, 40),
        text_color: tuple[int, int, int] = (255, 255, 255),
        font_size: int = 20,
        border_color: tuple[int, int, int] | None = None,
        border_width: int = 2,
        icon: pygame.Surface | None = None,
    ) -> None:
        super().__init__(width=width, height=height)
        self.text: str | Callable[[], str] = text
        self.on_click: Callable[[], None] | None = on_click
        self.bg_color: tuple[int, int, int] = bg_color
        self.hover_color: tuple[int, int, int] = hover_color
        self.press_color: tuple[int, int, int] = press_color
        self.text_color: tuple[int, int, int] = text_color
        self.font_size: int = font_size
        self.border_color: tuple[int, int, int] | None = border_color
        self.border_width: int = border_width
        self.icon: pygame.Surface | None = icon
        self.state: int = Button.NORMAL
        self._font: pygame.font.Font = pygame.font.Font(None, font_size)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for hover, press, and click detection."""
        if not self.visible:
            return False
        rect = self.get_rect()
        if event.type == pygame.MOUSEMOTION:
            if rect.collidepoint(event.pos):
                if self.state != Button.PRESSED:
                    self.state = Button.HOVER
            else:
                self.state = Button.NORMAL
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect.collidepoint(event.pos):
                self.state = Button.PRESSED
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.state == Button.PRESSED:
                self.state = Button.NORMAL
                if rect.collidepoint(event.pos) and self.on_click:
                    self.on_click()
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the button with the appropriate state color and centered text."""
        if not self.visible:
            return
        rect = self.get_rect()
        # Pick color based on state
        if self.state == Button.PRESSED:
            color = self.press_color
        elif self.state == Button.HOVER:
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(screen, color, rect)
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, rect, self.border_width)

        # Render text (bottom-aligned when icon is present, centered otherwise)
        display_text = self.text if isinstance(self.text, str) else self.text()
        lines = display_text.split("\n")
        line_height = self._font.get_linesize()
        total_h = len(lines) * line_height

        if self.icon is not None:
            bottom_pad = 6
            top_pad = 6
            avail_w = max(1, rect.width - 16)
            avail_h = max(1, rect.height - total_h - bottom_pad - top_pad - 4)
            iw, ih = self.icon.get_size()
            scale = min(avail_w / iw, avail_h / ih)
            scaled_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
            icon_surf = (
                self.icon
                if scaled_size == (iw, ih)
                else pygame.transform.smoothscale(self.icon, scaled_size)
            )
            icon_rect = icon_surf.get_rect(
                centerx=rect.centerx,
                centery=rect.top + top_pad + avail_h // 2,
            )
            screen.blit(icon_surf, icon_rect)
            start_y = rect.bottom - total_h - bottom_pad
        else:
            start_y = rect.centery - total_h // 2

        for i, line in enumerate(lines):
            line_surf = self._font.render(line, True, self.text_color)
            line_rect = line_surf.get_rect(
                centerx=rect.centerx,
                centery=start_y + i * line_height + line_height // 2
            )
            screen.blit(line_surf, line_rect)
