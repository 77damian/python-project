import pygame

from constants import *

class Camera:
    def __init__(self):
        self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.world_width, self.world_height = WORLD_WIDTH, WORLD_HEIGHT
        self.x, self.y = WORLD_WIDTH / 2, WORLD_HEIGHT/ 2
        self.zoom = 1.0
        self.min_zoom, self.max_zoom = 0.5, 3.0

    def clamp(self):
        view_height, view_width = self.screen_height / self.zoom, self.screen_width / self.zoom

        if view_width >= self.world_width:
            self.x = self.world_width / 2
        else:
            self.x = max(view_width / 2, min(self.world_width - view_width / 2, self.x))

        if view_height >= self.world_height:
            self.y = self.world_height / 2
        else:
            self.y = max(view_height / 2, min(self.world_height - view_height / 2, self.y))


    def set_zoom(self, zoom):
        self.zoom = max(self.min_zoom, min(self.max_zoom, zoom))
        self.clamp()

    def zoom_by(self, amount):
        self.set_zoom(self.zoom + amount)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.clamp()


    def world_to_screen(self, x, y):
        screen_x = (x - self.x) * self.zoom + self.screen_width / 2
        screen_y = (y - self.y) * self.zoom + self.screen_height / 2

        return screen_x, screen_y

    def world_rect_to_screen(self, rect):
        """
        Convert a world-space Rect to a screen-space Rect.
        """
        x, y = self.world_to_screen(rect.x, rect.y)

        return pygame.Rect(
            x,
            y,
            rect.width * self.zoom,
            rect.height * self.zoom
        )






