import sys

import pygame

from building.building import Building, Crystal
from constants import *
from camera import Camera
from map import Map
from enemies import Enemy, random_edge_position
from building.building_manager import BuildingManager

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

camera = Camera()

enemies = pygame.sprite.Group()
spawn_timer = 0.0

map_manager = Map(screen, camera)
build_manager = BuildingManager(screen, camera)

while True:
    dt = clock.tick(60) / 1000.0
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            camera.zoom_by(event.y * ZOOM_SPEED)

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
    map_manager.draw()
    build_manager.draw()


    for enemy in enemies:
        enemy.draw(screen, camera)
    if keys[pygame.K_x]:
        map_manager.draw_grid()




    pygame.display.flip()
