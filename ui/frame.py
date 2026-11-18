"""Frame container UI element — arranges children like a CSS flexbox div."""

import pygame

from .ui_element import UIElement


class Frame(UIElement):
    """Container that holds UI elements and arranges them.

    layout:
      "vertical"   — stack children top to bottom
      "horizontal"  — arrange children left to right
      "free"        — each child uses its own (x, y) relative to frame

    If width/height is None, the frame auto-sizes to fit its children.
    """

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        width: int | None = None,
        height: int | None = None,
        layout: str = "vertical",
        padding: int = 10,
        gap: int = 8,
        bg_color: tuple[int, int, int] | None = None,
        border_color: tuple[int, int, int] | None = None,
        border_width: int = 2,
        anchor: str | None = None,
    ) -> None:
        # Use 0 initially; will be recalculated if width/height is None
        super().__init__(x=x, y=y, width=width or 0, height=height or 0)
        self.children: list[UIElement] = []
        self.layout: str = layout
        self.padding: int = padding
        self.gap: int = gap
        self.bg_color: tuple[int, int, int] | None = bg_color
        self.border_color: tuple[int, int, int] | None = border_color
        self.border_width: int = border_width
        self.auto_width: bool = width is None
        self.auto_height: bool = height is None
        self.anchor: str | None = anchor  # "center", "top-center", "bottom-right", etc.
        self._anchor_target: tuple[int, int] | None = None  # (screen_width, screen_height)

    def set_anchor_target(self, screen_width: int, screen_height: int) -> None:
        """Set the screen dimensions used for anchor positioning."""
        self._anchor_target = (screen_width, screen_height)

    def add(self, element: UIElement, **kwargs: int) -> "Frame":
        """Add a child element. For 'free' layout, pass x=, y= as kwargs."""
        element.parent = self
        if self.layout == "free" and kwargs:
            element.x = kwargs.get("x", element.x)
            element.y = kwargs.get("y", element.y)
        self.children.append(element)
        self._layout_children()
        return self  # for chaining

    def remove(self, element: UIElement) -> None:
        """Remove a child element from this frame."""
        if element in self.children:
            self.children.remove(element)
            element.parent = None
            self._layout_children()

    def _layout_children(self) -> None:
        """Recalculate children positions based on layout mode."""
        if self.layout == "free":
            self._calc_auto_size_free()
            return

        visible = [c for c in self.children if c.visible]

        # --- First pass: position on main axis, measure cross axis ---
        cursor: int = self.padding
        max_cross: int = 0

        for i, child in enumerate(visible):
            cw, ch = child.get_size()
            if self.layout == "vertical":
                child.y = cursor
                cursor += ch + (self.gap if i < len(visible) - 1 else 0)
                max_cross = max(max_cross, cw)
            elif self.layout == "horizontal":
                child.x = cursor
                cursor += cw + (self.gap if i < len(visible) - 1 else 0)
                max_cross = max(max_cross, ch)

        # --- Auto-size ---
        if self.layout == "vertical":
            if self.auto_height:
                self.height = cursor + self.padding
            if self.auto_width:
                self.width = max_cross + 2 * self.padding
        elif self.layout == "horizontal":
            if self.auto_width:
                self.width = cursor + self.padding
            if self.auto_height:
                self.height = max_cross + 2 * self.padding

        # --- Second pass: center children on the cross axis ---
        for child in visible:
            cw, ch = child.get_size()
            if self.layout == "vertical":
                child.x = (self.width - cw) // 2
            elif self.layout == "horizontal":
                child.y = (self.height - ch) // 2

        self._apply_anchor()

    def _calc_auto_size_free(self) -> None:
        """Calculate auto-size for free layout based on children bounds."""
        if not self.auto_width and not self.auto_height:
            return
        max_r, max_b = 0, 0
        for child in self.children:
            if child.visible:
                cw, ch = child.get_size()
                max_r = max(max_r, child.x + cw)
                max_b = max(max_b, child.y + ch)
        if self.auto_width:
            self.width = max_r + self.padding
        if self.auto_height:
            self.height = max_b + self.padding
        self._apply_anchor()

    def _apply_anchor(self) -> None:
        """Position the frame based on its anchor within the screen."""
        if not self.anchor or not self._anchor_target:
            return
        sw, sh = self._anchor_target
        parts = self.anchor.split("-")

        # Vertical
        if "top" in parts:
            self.y = 0
        elif "bottom" in parts:
            self.y = sh - self.height
        elif "center" in parts and len(parts) == 1:
            self.y = (sh - self.height) // 2
            self.x = (sw - self.width) // 2
            return
        else:
            # default: keep current y
            pass

        # Horizontal
        if "left" in parts:
            self.x = 0
        elif "right" in parts:
            self.x = sw - self.width
        elif "center" in parts:
            self.x = (sw - self.width) // 2

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Propagate events to children in reverse order (top-most first)."""
        if not self.visible:
            return False
        # Children in reverse order (top-most first)
        for child in reversed(self.children):
            if child.visible and child.handle_event(event):
                return True
        return False

    def update(self, dt: float) -> None:
        """Update all visible children and re-layout."""
        if not self.visible:
            return
        for child in self.children:
            if child.visible:
                child.update(dt)
        # Re-layout in case dynamic labels changed size
        self._layout_children()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw background, border, and all visible children."""
        if not self.visible:
            return
        rect = self.get_rect()
        if self.bg_color:
            pygame.draw.rect(screen, self.bg_color, rect)
        if self.border_color:
            pygame.draw.rect(screen, self.border_color, rect, self.border_width)
        for child in self.children:
            if child.visible:
                child.draw(screen)
