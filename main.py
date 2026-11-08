import sys

import pygame

from building.building import Building, Crystal
from constants import *
from camera import Camera
from map import Map
from enemies import Enemy, random_edge_position
from building.building_manager import BuildingManager
from ui.ui_manager import UIManager
from ui.screens.main_menu import create_main_menu
from ui.screens.level_select import create_level_select
from ui.screens.hud import create_hud

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

camera = Camera()

enemies = pygame.sprite.Group()
spawn_timer = 0.0

map_manager = Map(screen, camera)
build_manager = BuildingManager(screen, camera)

# --- UI Setup ---
ui_manager = UIManager(screen)

# Game state dict — shared with HUD so labels auto-update
game_state = {
    "wave": 1,
    "max_waves": 10,
    "gold": 200,
    "tower_hp": 100,
    "tower_max_hp": 100,
    "selected_building": None,
    "paused": False,
}

# Create all screens
create_main_menu(ui_manager)
create_level_select(ui_manager)
create_hud(ui_manager, game_state)

# Start on main menu
ui_manager.set_screen("main_menu")


while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Let UI handle event first — if consumed, skip game input
        if ui_manager.handle_event(event):
            continue

        # Game-specific events (only when in "game" screen)
        if ui_manager.get_active_screen_name() == "game":
            if event.type == pygame.MOUSEWHEEL and not game_state.get("paused", False):
                camera.zoom_by(event.y * ZOOM_SPEED)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and not game_state.get("paused", False):
                    hud_overlay = ui_manager.overlays.get("hud")
                    if hud_overlay and hasattr(hud_overlay, "toggle_build_panel"):
                        hud_overlay.toggle_build_panel()
                elif event.key == pygame.K_ESCAPE:
                    hud_overlay = ui_manager.overlays.get("hud")
                    if hud_overlay and hasattr(hud_overlay, "toggle_pause"):
                        hud_overlay.toggle_pause()

    current_screen = ui_manager.get_active_screen_name()

    # --- GAME SCREEN LOGIC ---
    if current_screen == "game":
        # Show HUD overlay during gameplay
        ui_manager.show_overlay("hud")

        is_paused = game_state.get("paused", False)

        if not is_paused:
            # Check if building selected via UI
            if game_state.get("selected_building") is not None:
                build_manager.selected_building = Building(-1000, -1000)
                game_state["selected_building"] = None

            keys = pygame.key.get_pressed()
            camera_speed = CAMERA_SPEED * dt / camera.zoom

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                camera.move(-camera_speed, 0)
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                camera.move(camera_speed, 0)
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                camera.move(0, -camera_speed)
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                camera.move(0, camera_speed)

            build_manager.handle_keys(keys)

            spawn_timer += dt
            if spawn_timer >= ENEMY_SPAWN_INTERVAL and len(enemies) < MAX_ENEMIES:
                spawn_timer = 0.0
                enemy = Enemy(*random_edge_position())
                enemy.set_target(*TARGET_POS)
                enemies.add(enemy)

            map_manager.update(pygame.mouse.get_pos())
            enemies.update(dt)
            build_manager.update(dt, pygame.mouse.get_pos())

        # --- Draw game world ---
        screen.fill("black")
        map_manager.draw()
        build_manager.draw()

        for enemy in enemies:
            enemy.draw(screen, camera)

        if not is_paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                map_manager.draw_grid()
        else:
            # Semi-transparent dark overlay over world when paused
            dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            dim.fill((0, 0, 0, 140))
            screen.blit(dim, (0, 0))

    else:
        # Menu screens — dark background
        ui_manager.hide_overlay("hud")
        screen.fill((10, 10, 20))

    # --- Draw UI on top ---
    ui_manager.update(dt)
    ui_manager.draw()

    pygame.display.flip()
