

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

CAMERA_SPEED = 500
ZOOM_SPEED = 0.25

WORLD_WIDTH = 3200 # x32
WORLD_HEIGHT = 1280 # x32


TERRAIN_COLORS = {"W": "cyan", "G": "green"}

TILE_SIZE = 32

TARGET_POS = (WORLD_WIDTH / 2, WORLD_HEIGHT / 2)  # enemies head here

ENEMY_SPAWN_INTERVAL = 2.5  # seconds
MAX_ENEMIES = 30

# Buildings (TEMPORARY)

BUILDING_DICTIONARY = {
    1: {"color": "grey", "size": 10, "type": "wall"},
    2: {"color": "red", "size": 20, "type": "tower"},
}
