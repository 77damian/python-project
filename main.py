import sys

import pygame

from constants import *
from camera import Camera
from map import map

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

camera = Camera()


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

    for y in range(len(map)):
        for x in range(len(map[0])):
            sx, sy = camera.world_to_screen(x, y)
            if map[y][x] == 0:
                color = "cyan"
            else:
                color = "green"

            tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen_rect = camera.world_rect_to_screen(tile_rect)
            pygame.draw.rect(screen, color, screen_rect)


    # Draw a grid
    grid_size = 32

    for x in range(0, WORLD_WIDTH + 1, grid_size):
        sx, sy = camera.world_to_screen(x, 0)
        ex, ey = camera.world_to_screen(x, WORLD_HEIGHT)

        pygame.draw.line(
            screen,
            (80, 140, 80),
            (sx, sy),
            (ex, ey),
            1
        )

    for y in range(0, WORLD_HEIGHT + 1, grid_size):
        sx, sy = camera.world_to_screen(0, y)
        ex, ey = camera.world_to_screen(WORLD_WIDTH, y)

        pygame.draw.line(
            screen,
            (80, 140, 80),
            (sx, sy),
            (ex, ey),
            1
        )


    pygame.display.flip()
