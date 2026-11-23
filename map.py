from pathlib import Path

import pygame

from constants import *

NEIGHBOR_BITS = (
    (0, -1, 1),    # N
    (0, 1, 2),     # S
    (-1, 0, 4),    # W
    (1, 0, 8),     # E
    (-1, -1, 16),  # NW
    (1, -1, 32),   # NE
    (-1, 1, 64),   # SW
    (1, 1, 128),   # SE
)


class Tile:
    def __init__(self, x, y, terrain, structure=None):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.structure = structure
        self.sprite_key = None
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)


class Map:
    _cache = {}          # parsed maps by path
    _base_tiles = None   # unscaled 32x32 surfaces sliced from TileSet_V2.png
    _scaled_cache = {}   # (sprite_key, width, height) -> scaled pygame.Surface

    def __init__(self, screen, camera, path="assets/maps/level1.txt"):
        self.screen = screen
        self.camera = camera
        self.tiles = self.load_tileset()
        self.board = self.load_map(path)
        self.rows = len(self.board)
        self.cols = len(self.board[0])
        self.crystal_tile = self.find_crystal()
        self.mouse_pos = None

    @classmethod
    def load_tileset(cls):
        if cls._base_tiles is None:
            tileset_path = Path(__file__).parent / TILESET_PATH
            sheet = pygame.image.load(tileset_path).convert_alpha()
            cls._base_tiles = {
                name: sheet.subsurface(pygame.Rect(rect)).copy()
                for name, rect in TILE_ATLAS.items()
            }
        return cls._base_tiles

    @classmethod
    def get_scaled_tile(cls, sprite_key, width, height):
        cache_key = (sprite_key, width, height)
        surf = cls._scaled_cache.get(cache_key)
        if surf is None:
            base = cls._base_tiles[sprite_key]
            if width == TILE_SIZE and height == TILE_SIZE:
                surf = base
            else:
                surf = pygame.transform.scale(base, (width, height))
            cls._scaled_cache[cache_key] = surf
        return surf

    @staticmethod
    def _pick_grass_variant(x, y):
        # Deterministic natural distribution: mostly grass_default_1 with occasional tufts
        h = ((x * 73856093) ^ (y * 19349663)) % 20
        if h == 0:
            return "grass_default_2"
        if h == 1:
            return "grass_default_3"
        if h == 2:
            return "grass_default_4"
        return "grass_default_1"

    @classmethod
    def _compute_water_sprite(cls, board, x, y):
        height = len(board)
        width = len(board[0])
        mask = 0

        for dx, dy, bit in NEIGHBOR_BITS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and board[ny][nx].terrain == "G":
                mask |= bit

        if mask == 0:
            return "water_default"

        exact_key = f"water_grass_{mask}"
        if exact_key in TILE_ATLAS:
            return exact_key

        cardinal_mask = mask & 15
        if cardinal_mask:
            cardinal_key = f"water_grass_{cardinal_mask}"
            if cardinal_key in TILE_ATLAS:
                return cardinal_key

        return "water_default"

    @classmethod
    def assign_tile_sprites(cls, board):
        for y, row in enumerate(board):
            for x, tile in enumerate(row):
                if tile.terrain == "W":
                    tile.sprite_key = cls._compute_water_sprite(board, x, y)
                else:
                    tile.sprite_key = cls._pick_grass_variant(x, y)

    @classmethod
    def load_map(cls, path):
        path = Path(__file__).parent / path
        if path not in cls._cache:
            with open(path, encoding="utf-8") as f:
                board = cls.parse_map(f.read(), path.name)
            cls.assign_tile_sprites(board)
            cls._cache[path] = board
        return cls._cache[path]

    @staticmethod
    def parse_map(text, name="<map>"):
        board = []

        for line_no, line in enumerate(text.splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            row = []
            for x, token in enumerate(line.split()):
                terrain, structure = token[0], token[1:] or None
                if terrain not in TERRAIN_COLORS:
                    raise ValueError(f"{name}:{line_no}, tile {x + 1} ('{token}'): unknown terrain")
                if structure not in (None, CRYSTAL_TOKEN):
                    raise ValueError(f"{name}:{line_no}, tile {x + 1} ('{token}'): unknown structure")
                row.append(Tile(x, len(board), terrain, structure))

            if board and len(row) != len(board[0]):
                raise ValueError(f"{name}:{line_no}: row has {len(row)} tiles, expected {len(board[0])}")
            board.append(row)

        if not board:
            raise ValueError(f"{name}: map is empty")
        return board

    def is_area_buildable(self, rect):
        start_col = int(rect.left // TILE_SIZE)
        end_col = int((rect.right - 1) // TILE_SIZE)
        start_row = int(rect.top // TILE_SIZE)
        end_row = int((rect.bottom - 1) // TILE_SIZE)

        if start_col < 0 or start_row < 0 or end_col >= self.cols or end_row >= self.rows:
            return False

        for row in range(start_row, end_row + 1):
            for col in range(start_col, end_col + 1):
                tile = self.board[row][col]
                if tile.terrain != "G" or tile.structure is not None:
                    return False

        return True

    def find_crystal(self):
        crystals = [tile for row in self.board for tile in row if tile.structure == CRYSTAL_TOKEN]
        if len(crystals) != 1:
            raise ValueError(f"map must contain exactly one crystal, found {len(crystals)}")
        return crystals[0]

    def draw(self):
        zoom = self.camera.zoom
        half_view_w = (SCREEN_WIDTH / 2) / zoom
        half_view_h = (SCREEN_HEIGHT / 2) / zoom

        start_col = max(0, int((self.camera.x - half_view_w) // TILE_SIZE))
        end_col = min(self.cols - 1, int((self.camera.x + half_view_w) // TILE_SIZE) + 1)
        start_row = max(0, int((self.camera.y - half_view_h) // TILE_SIZE))
        end_row = min(self.rows - 1, int((self.camera.y + half_view_h) // TILE_SIZE) + 1)

        for row_idx in range(start_row, end_row + 1):
            row = self.board[row_idx]
            wy1 = row_idx * TILE_SIZE
            wy2 = wy1 + TILE_SIZE
            _, sy1 = self.camera.world_to_screen(0, wy1)
            _, sy2 = self.camera.world_to_screen(0, wy2)
            iy1 = round(sy1)
            th = round(sy2) - iy1
            if th <= 0:
                continue

            for col_idx in range(start_col, end_col + 1):
                tile = row[col_idx]
                wx1 = col_idx * TILE_SIZE
                sx1, _ = self.camera.world_to_screen(wx1, 0)
                sx2, _ = self.camera.world_to_screen(wx1 + TILE_SIZE, 0)
                ix1 = round(sx1)
                tw = round(sx2) - ix1
                if tw <= 0:
                    continue

                surf = self.get_scaled_tile(tile.sprite_key, tw, th)
                self.screen.blit(surf, (ix1, iy1))

    def draw_grid(self):
        grid_size = TILE_SIZE

        half_view_w = (SCREEN_WIDTH / 2) / self.camera.zoom
        half_view_h = (SCREEN_HEIGHT / 2) / self.camera.zoom

        min_wx = self.camera.x - half_view_w
        max_wx = self.camera.x + half_view_w
        min_wy = self.camera.y - half_view_h
        max_wy = self.camera.y + half_view_h

        start_x = int(min_wx // grid_size) * grid_size
        end_x = int(max_wx // grid_size + 1) * grid_size
        start_y = int(min_wy // grid_size) * grid_size
        end_y = int(max_wy // grid_size + 1) * grid_size

        for x in range(start_x, end_x + grid_size, grid_size):
            sx1, sy1 = self.camera.world_to_screen(x, min_wy)
            sx2, sy2 = self.camera.world_to_screen(x, max_wy)
            pygame.draw.line(
                self.screen,
                (80, 140, 80),
                (round(sx1), round(sy1)),
                (round(sx2), round(sy2)),
                1,
            )

        for y in range(start_y, end_y + grid_size, grid_size):
            sx1, sy1 = self.camera.world_to_screen(min_wx, y)
            sx2, sy2 = self.camera.world_to_screen(max_wx, y)
            pygame.draw.line(
                self.screen,
                (80, 140, 80),
                (round(sx1), round(sy1)),
                (round(sx2), round(sy2)),
                1,
            )

    def update(self, mouse_pos):
        self.mouse_pos = mouse_pos