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
TOWER_BASE_IMAGES = {
    1: "assets/towers/base/towerBaseLvl1.png",
    2: "assets/towers/base/towerBaseLvl2.png",
    3: "assets/towers/base/towerBaseLvl3.png",
    4: "assets/towers/base/towerBaseLvl4.png",
}

TOWER_HEAD_IMAGES = {
    "default": "assets/towers/head/towerHeadDefault.png",
    "area": "assets/towers/head/towerHeadArea.png",
    "long": "assets/towers/head/towerHeadLong.png",
}

# Ścieżki do grafik pocisków
BULLET_IMAGES = {
    "default": "assets/bullets/bulletDefault.png",
    "rocket_small": "assets/bullets/bulletRocketRangeSmall.png",
    "rocket_big": "assets/bullets/bulletRocketRangeBig.png",
}

TOWERS_DATA = {
    1: {
        "name": "BaseTower",
        "head": "default",
        "head_img": TOWER_HEAD_IMAGES["default"],
        "bullet_img": BULLET_IMAGES["default"],
        "damage": 10,
        "range": 150,
        "fire_rate": 1.0,
        "bullet_speed": 300,
        "cost": 50,
    },
}

# BUILDING_DICTIONARY = {
#     1: {"color": "grey", "type": "wall"},
#     2: {"color": "red", "type": "tower"},
# }
