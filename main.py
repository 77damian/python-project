import sys

import pygame


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

while True:
    dt = clock.tick(60) / 1000.0
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

