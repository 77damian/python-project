"""Manages the active level state, entities, and level reset."""

import pygame

from building.building import Crystal
from building.building_manager import BuildingManager
from constants import CRYSTAL_HEALTH


class LevelManager:
    """Holds all runtime state for the current level and handles resetting it."""

    def __init__(self, screen, camera, map_manager):
        self.screen = screen
        self.camera = camera
        self.map_manager = map_manager

        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.spawn_timer = 0.0
        self.wave_enemies_total = 5
        self.wave_enemies_spawned = 0
        self.wave_delay_timer = 0.0

        self.build_manager = None
        self.crystal = None

        self.game_state = {
            "wave": 1,
            "max_waves": 10,
            "gold": 200,
            "tower_hp": CRYSTAL_HEALTH,
            "tower_max_hp": CRYSTAL_HEALTH,
            "selected_building": None,
            "paused": False,
            "game_over": False,
            "level_won": False,
            "restart_requested": False,
            "selected_level": 1,
        }

        self.reset()

    def reset(self):
        """Reset all level entities and state to initial values."""
        self.enemies.empty()
        self.bullets.empty()
        self.spawn_timer = 0.0
        self.wave_enemies_total = 5
        self.wave_enemies_spawned = 0
        self.wave_delay_timer = 0.0

        self.map_manager.load_level(self.game_state["selected_level"])
        self.build_manager = BuildingManager(self.screen, self.camera, self.map_manager)
        self.crystal = Crystal(self.map_manager.crystal_tile.x, self.map_manager.crystal_tile.y)
        self.build_manager.add_building(self.crystal)

        self.game_state["wave"] = 1
        self.game_state["gold"] = 200
        self.game_state["tower_hp"] = CRYSTAL_HEALTH
        self.game_state["tower_max_hp"] = CRYSTAL_HEALTH
        self.game_state["selected_building"] = None
        self.game_state["paused"] = False
        self.game_state["game_over"] = False
        self.game_state["level_won"] = False
        self.game_state["restart_requested"] = False
