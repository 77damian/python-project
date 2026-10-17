from pathlib import Path

import pygame

from constants import *


class Tile:
    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)


class Map:
    _cache = {}  # parsed maps by path, so each file is read only once

    def __init__(self, screen, camera, path="assets/maps/level1.txt"):
        self.screen = screen
        self.camera = camera
        self.board = self.load_map(path)
        self.mouse_pos = None

    # loads map from file to cache
    @classmethod
    def load_map(cls, path):
        path = Path(__file__).parent / path
        if path not in cls._cache:
            with open(path, encoding="utf-8") as f:
                cls._cache[path] = cls.parse_map(f.read(), path.name)
        return cls._cache[path]

    # builds the tile grid (board[y][x]) from map text
    @staticmethod
    def parse_map(text, name="<map>"):
        board = []

        for line_no, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            # skip blank lines and comments
            if not line or line.startswith("#"):
                continue

            row = []
            for x, token in enumerate(line.split()):
                if token not in TERRAIN_COLORS:
                    raise ValueError(f"{name}:{line_no}, tile {x + 1} ('{token}'): unknown terrain")
                row.append(Tile(x, len(board), token))

            # all rows must be the same length
            if board and len(row) != len(board[0]):
                raise ValueError(f"{name}:{line_no}: row has {len(row)} tiles, expected {len(board[0])}")
            board.append(row)

        if not board:
            raise ValueError(f"{name}: map is empty")
        return board

    # draws terrain
    def draw(self):
        for row in self.board:
            for tile in row:
                screen_rect = self.camera.world_rect_to_screen(tile.rect)
                pygame.draw.rect(self.screen, TERRAIN_COLORS[tile.terrain], screen_rect)

    def draw_grid(self):
        grid_size = 32

        # 1. Calculate what part of the world is currently visible on screen
        half_view_w = (SCREEN_WIDTH / 2) / self.camera.zoom
        half_view_h = (SCREEN_HEIGHT / 2) / self.camera.zoom

        min_wx = self.camera.x - half_view_w
        max_wx = self.camera.x + half_view_w
        min_wy = self.camera.y - half_view_h
        max_wy = self.camera.y + half_view_h

        # 2. Snap bounds to the nearest grid lines
        start_x = int(min_wx // grid_size) * grid_size
        end_x = int(max_wx // grid_size + 1) * grid_size
        start_y = int(min_wy // grid_size) * grid_size
        end_y = int(max_wy // grid_size + 1) * grid_size

        # 3. Draw only the vertical lines inside the viewport
        for x in range(start_x, end_x + grid_size, grid_size):
            sx1, sy1 = self.camera.world_to_screen(x, min_wy)
            sx2, sy2 = self.camera.world_to_screen(x, max_wy)

            pygame.draw.line(
                self.screen,
                (80, 140, 80),
                (round(sx1), round(sy1)),  # round() prevents sub-pixel thickness jitter
                (round(sx2), round(sy2)),
                1
            )

        # 4. Draw only the horizontal lines inside the viewport
        for y in range(start_y, end_y + grid_size, grid_size):
            sx1, sy1 = self.camera.world_to_screen(min_wx, y)
            sx2, sy2 = self.camera.world_to_screen(max_wx, y)

            pygame.draw.line(
                self.screen,
                (80, 140, 80),
                (round(sx1), round(sy1)),
                (round(sx2), round(sy2)),
                1
            )

    def update(self, mouse_pos):
        self.mouse_pos = mouse_pos

