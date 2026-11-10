"""Base class for all UI elements."""

import pygame


class UIElement:
    """Base class for all UI elements."""

    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.visible: bool = True
        self.parent: "UIElement | None" = None  # set by Frame when added

    def draw(self, screen: pygame.Surface) -> None:
        """Override in subclasses."""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle pygame event. Return True if consumed."""
        return False

    def update(self, dt: float) -> None:
        """Update logic per frame."""
        pass

    def get_size(self) -> tuple[int, int]:
        """Return the (width, height) of this element."""
        return (self.width, self.height)

    def get_absolute_position(self) -> tuple[int, int]:
        """Get position in screen space (traversing parents)."""
        abs_x, abs_y = self.x, self.y
        parent = self.parent
        while parent:
            abs_x += parent.x
            abs_y += parent.y
            parent = parent.parent
        return abs_x, abs_y

    def get_rect(self) -> pygame.Rect:
        """Return a pygame.Rect in absolute screen coordinates."""
        ax, ay = self.get_absolute_position()
        return pygame.Rect(ax, ay, self.width, self.height)

    def show(self) -> None:
        """Make this element visible."""
        self.visible = True

    def hide(self) -> None:
        """Make this element invisible."""
        self.visible = False

    def toggle(self) -> None:
        """Toggle visibility."""
        self.visible = not self.visible
