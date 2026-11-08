"""UI Manager — handles screen transitions and overlay rendering.

The UIManager keeps a registry of named screens (Frame objects) and named
overlays.  Only the *active* screen receives events and is drawn each frame.
Overlays are drawn on top of the active screen and receive events first.
"""

import pygame
import sys
from typing import Dict, Optional, Set

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ui.frame import Frame


class UIManager:
    """Manages screen transitions and active UI state.

    Screens are registered by name.  Only the active screen receives events
    and draws.  Overlay screens (like HUD) are drawn on TOP of the active
    screen.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """Initialise the UI manager.

        Args:
            screen: The main pygame display surface.
        """
        self.screen: pygame.Surface = screen
        self.screens: Dict[str, Frame] = {}
        self.overlays: Dict[str, Frame] = {}
        self.active_screen: Optional[str] = None
        self.active_overlays: Set[str] = set()

    def add_screen(self, name: str, frame: Frame) -> None:
        """Register a screen.

        Args:
            name:  Unique identifier for the screen.
            frame: Root Frame that represents the screen.
        """
        self.screens[name] = frame

    def add_overlay(self, name: str, frame: Frame) -> None:
        """Register an overlay (like HUD).

        Args:
            name:  Unique identifier for the overlay.
            frame: Root Frame that represents the overlay.
        """
        self.overlays[name] = frame

    def set_screen(self, name: str) -> None:
        """Switch to a screen by name.

        Args:
            name: Identifier previously passed to :meth:`add_screen`.
        """
        self.active_screen = name

    def show_overlay(self, name: str) -> None:
        """Make an overlay visible.

        Args:
            name: Identifier previously passed to :meth:`add_overlay`.
        """
        self.active_overlays.add(name)

    def hide_overlay(self, name: str) -> None:
        """Hide an overlay (no-op if already hidden).

        Args:
            name: Identifier previously passed to :meth:`add_overlay`.
        """
        self.active_overlays.discard(name)

    def get_active_screen_name(self) -> Optional[str]:
        """Return the name of the currently active screen."""
        return self.active_screen

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Pass *event* to active overlays first, then to the active screen.

        Returns:
            ``True`` if any UI element consumed the event.
        """
        # Overlays get priority (they are rendered on top).
        for name in list(self.active_overlays):
            overlay = self.overlays.get(name)
            if overlay and overlay.handle_event(event):
                return True
        # Then the active screen.
        if self.active_screen and self.active_screen in self.screens:
            return self.screens[self.active_screen].handle_event(event)
        return False

    def update(self, dt: float) -> None:
        """Tick the active screen and visible overlays.

        Args:
            dt: Delta-time in seconds since the last frame.
        """
        if self.active_screen and self.active_screen in self.screens:
            self.screens[self.active_screen].update(dt)
        for name in self.active_overlays:
            overlay = self.overlays.get(name)
            if overlay:
                overlay.update(dt)

    def draw(self) -> None:
        """Draw the active screen, then every visible overlay on top."""
        if self.active_screen and self.active_screen in self.screens:
            self.screens[self.active_screen].draw(self.screen)
        for name in self.active_overlays:
            overlay = self.overlays.get(name)
            if overlay:
                overlay.draw(self.screen)
