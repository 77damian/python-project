import random

import pygame

from constants import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)  # position in world space
        self.target = None
        self.speed = 60  # world px/s

        # placeholder graphics
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, "red", (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 2)
        self.rect = self.image.get_rect(center=(round(x), round(y)))

    def set_target(self, x, y):
        self.target = pygame.Vector2(x, y)

    def update(self, dt):
        if self.target is None:
            return

        to_target = self.target - self.pos
        step = self.speed * dt

        if to_target.length() <= step:
            self.pos.update(self.target)
            self.kill()  # reached the target
        else:
            self.pos += to_target.normalize() * step
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    # enemies draw themselves
    def draw(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)
        screen.blit(pygame.transform.scale(self.image, screen_rect.size), screen_rect)


# random point on the border of the world
def random_edge_position():
    side = random.choice("NSWE")
    if side == "N":
        return random.uniform(0, WORLD_WIDTH), 0
    if side == "S":
        return random.uniform(0, WORLD_WIDTH), WORLD_HEIGHT
    if side == "W":
        return 0, random.uniform(0, WORLD_HEIGHT)
    return WORLD_WIDTH, random.uniform(0, WORLD_HEIGHT)
