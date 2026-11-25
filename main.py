import sys

import pygame

from constants import *
from camera import Camera
from map import Map
from enemies import *
from level_manager import LevelManager
from ui.ui_manager import UIManager
from ui.screens.main_menu import create_main_menu
from ui.screens.level_select import create_level_select
from ui.screens.hud import create_hud
from ui.screens.level_end import create_level_end

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")

camera = Camera()

map_manager = Map(screen, camera)
ui_manager = UIManager(screen)
level = LevelManager(screen, camera, map_manager)
game_state = level.game_state

# Create all screens
create_main_menu(ui_manager)
create_level_select(ui_manager, game_state)
create_hud(ui_manager, game_state)
create_level_end(ui_manager, game_state)

# Start on main menu
ui_manager.set_screen("main_menu")


while True:
    dt = clock.tick(60) / 1000.0

    place_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Let UI handle event first — if consumed, skip game input
        if ui_manager.handle_event(event):
            continue

        # Game-specific events (only when in "game" screen)
        if ui_manager.get_active_screen_name() == "game":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_state.get("paused", False):
                place_clicked = True
            elif event.type == pygame.MOUSEWHEEL and not game_state.get("paused", False):
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

    if game_state.get("restart_requested"):
        level.reset()

    # --- GAME SCREEN LOGIC ---
    if current_screen == "game":
        # Show HUD overlay during gameplay
        ui_manager.show_overlay("hud")
        is_paused = game_state.get("paused", False)

        if not is_paused:
            # Check if building selected via UI
            if game_state.get("clear_building"):
                level.build_manager.clear_selection()
                game_state["clear_building"] = False

            if game_state.get("selected_building") is not None:
                level.build_manager.select_building(game_state["selected_building"])
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

            level.build_manager.handle_keys(keys, place_clicked, game_state)

            level.spawn_timer += dt
            if level.spawn_timer >= ENEMY_SPAWN_INTERVAL and len(level.enemies) < MAX_ENEMIES:
                level.spawn_timer = 0.0
                level.enemies.add(spawn_enemy(level.crystal))

            alive_before = list(level.enemies)
            map_manager.update(pygame.mouse.get_pos())
            level.enemies.update(dt, level.bullets)
            level.bullets.update(dt)
            level.build_manager.update(dt, pygame.mouse.get_pos(), level.enemies, level.bullets)

            for enemy in alive_before:
                if not enemy.alive():
                    game_state["gold"] += getattr(enemy, "gold_reward", 10)
            game_state["tower_hp"] = max(0, level.crystal.health)
            if level.crystal.health <= 0 and not game_state["game_over"]:
                game_state["game_over"] = True
                game_state["level_won"] = False
                ui_manager.set_screen("level_end")

        # --- Draw game world ---
        screen.fill("black")
        map_manager.draw()
        level.build_manager.draw()

        for enemy in level.enemies:
            enemy.draw(screen, camera)
        for bullet in level.bullets:
            bullet.draw(screen, camera)
        if not is_paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_x]:
                map_manager.draw_grid()
        else:
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
