import pygame

from constants import *
from .building import Building
from towers.towers import BaseTower, LongTower, AreaTower


class BuildingManager:
    BUILDING_TYPES = {
        1: BaseTower,
        2: LongTower,
        3: AreaTower
    }
    BUILDING_COSTS = {
        1: 50,
        2: 80,
        3: 100,
    }

    def __init__(self, screen, camera, map_manager):
        self.buildings = pygame.sprite.Group()

        self.selected_building = None
        self.selected_building_id = None
        self.screen = screen
        self.camera = camera
        self.map_manager = map_manager
        self.mouse_clicked = False

    def get_building_at_grid(self, world_x, world_y):
        for building in self.buildings:
            if building.world_x == world_x and building.world_y == world_y:
                return building
        return None

    def can_place_building(self, building):
        if not self.map_manager.is_area_buildable(building.rect):
            return False

        for existing in self.buildings:
            if building.rect.colliderect(existing.rect):
                return False

        return True

    def select_building(self, building_id):
        building_cls = self.BUILDING_TYPES.get(building_id)
        if building_cls is not None:
            self.selected_building_id = building_id
            self.selected_building = building_cls(-1000, -1000)

    def clear_selection(self):
        self.selected_building = None
        self.selected_building_id = None

    def add_building(self, building):
        self.buildings.add(building)

    def update(self, dt, mouse_pos, enemies=None, bullets=None):
        self.buildings.update(dt, enemies, bullets)

        if self.selected_building:
            # 1. Convert screen mouse position to world coordinates
            world_x, world_y = self.camera.screen_to_world(mouse_pos[0], mouse_pos[1])

            # 2. Snap coordinates to the grid
            grid_x = (world_x // TILE_SIZE) * TILE_SIZE
            grid_y = (world_y // TILE_SIZE) * TILE_SIZE

            # 3. Move only the preview building
            self.selected_building.change_location(grid_x, grid_y)

    def draw(self):
        for building in self.buildings:
            building.draw(self.screen, self.camera)
        if self.selected_building:
            can_place = self.can_place_building(self.selected_building)
            self.selected_building.draw_preview(self.screen, self.camera, can_place)

    def handle_keys(self, keys, place_clicked=False, game_state=None):
        if keys[pygame.K_1]:
            self.select_building(1)
        if keys[pygame.K_2]:
            self.select_building(2)
        if keys[pygame.K_3]:
            self.select_building(3)

        if place_clicked and self.selected_building and self.can_place_building(self.selected_building):
            cost = self.BUILDING_COSTS.get(self.selected_building_id, 0)
            if game_state is None or game_state["gold"] >= cost:
                if game_state is not None:
                    game_state["gold"] -= cost
                self.buildings.add(self.selected_building)
                self.select_building(self.selected_building_id)
