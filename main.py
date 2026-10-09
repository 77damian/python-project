import sys

import pygame

from constants import *
from camera import Camera

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

camera = Camera()

objects = [
    pygame.Rect(500, 400, 200, 150),
    pygame.Rect(1000, 700, 300, 100),
    pygame.Rect(1800, 300, 150, 300),
    pygame.Rect(2400, 1400, 250, 200),
]

while True:
    dt = clock.tick(60) / 1000.0
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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

        # Draw a grid
    grid_size = 100

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

    for obj in objects:
        screen_obj = camera.world_rect_to_screen(obj)

        pygame.draw.rect(
            screen,
            (200, 80, 80),
            screen_obj
        )

    pygame.display.flip()
