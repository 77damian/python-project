

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

CAMERA_SPEED = 500
ZOOM_SPEED = 0.25

WORLD_WIDTH = 3200 # x32
WORLD_HEIGHT = 2048 # x32


TERRAIN_COLORS = {"W": "cyan", "G": "green"}

TILE_SIZE = 32

CRYSTAL_TOKEN = "C"
CRYSTAL_HEALTH = 1000

ENEMY_SPAWN_INTERVAL = 2.5  # seconds
MAX_ENEMIES = 30

# world px; enemy counts as "in range" when it is this close to its attack range
RANGE_TOLERANCE = 0.5

# Buildings (TEMPORARY)

BUILDING_DICTIONARY = {
    1: {"color": "grey", "type": "wall"},
    2: {"color": "red", "type": "tower"},
}
