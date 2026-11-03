import pygame

from constants import *

class Building(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y):
        super().__init__()
        self.world_x, self.world_y = world_x, world_y
        self.x, self.y = self.world_x*TILE_SIZE, self.world_y*TILE_SIZE
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.image.fill((255, 0, 0, 150))


    def update(self, dt):
        pass


    def draw(self, screen, camera):
        pygame.draw.rect(screen, "red", camera.world_rect_to_screen(self.rect))

    def draw_preview(self, screen, camera):
        pygame.draw.rect(screen, (0,0,255, 120), camera.world_rect_to_screen(self.rect))

    def change_location(self, x, y):
        self.x = x
        self.y = y
        self.rect.topleft = (self.x, self.y)
