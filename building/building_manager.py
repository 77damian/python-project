import pygame

from constants import *

from .building import Building

class BuildingManager:
    def __init__(self, screen, camera):
        self.buildings = pygame.sprite.Group()

        self.selected_building = None
        self.screen = screen
        self.camera = camera
        self.mouse_clicked = False

    def add_building(self, building):
        self.buildings.add(building)

    def update(self, dt, mouse_pos):
        self.buildings.update(dt)

        if self.selected_building:
            # 1. Convert screen mouse position to world coordinates
            world_x, world_y = self.camera.screen_to_world(mouse_pos[0], mouse_pos[1])

            # 2. Snap coordinates to the grid (optional, but recommended for tile games)
            grid_x = (world_x // TILE_SIZE) * TILE_SIZE
            grid_y = (world_y // TILE_SIZE) * TILE_SIZE

            # 3. Move only the preview building
            self.selected_building.change_location(grid_x, grid_y)



    def draw(self):
        for building in self.buildings:
            building.draw(self.screen, self.camera)
        if self.selected_building:
            self.selected_building.draw_preview(self.screen, self.camera)

    def handle_keys(self, keys):
        if keys[pygame.K_1]:
            self.selected_building = Building(-1000, -1000)
        if keys[pygame.K_2]:
            self.selected_building = Building(-1000, -1000)

        mouse_pressed = pygame.mouse.get_pressed()[0]

        if mouse_pressed and not self.mouse_clicked and self.selected_building:
            self.buildings.add(self.selected_building)
            self.selected_building = Building(-1000, -1000)

        self.mouse_clicked = mouse_pressed


