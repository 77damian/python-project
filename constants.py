
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

CAMERA_SPEED = 500
ZOOM_SPEED = 0.25

WORLD_WIDTH = 3200 # x32
WORLD_HEIGHT = 2048 # x32

TERRAIN_COLORS = {"W": "cyan", "G": "green"}

TILE_SIZE = 32
tile_size = TILE_SIZE

CRYSTAL_TOKEN = "C"
CRYSTAL_HEALTH = 1000

ENEMY_SPAWN_INTERVAL = 2.5  # seconds
MAX_ENEMIES = 30

# world px; enemy counts as "in range" when it is this close to its attack range
RANGE_TOLERANCE = 0.5

SPRITE_ANGLE_OFFSET = -90

TILESET_PATH = "assets/TileSet_V2.png"

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

BULLET_FIRE_IMAGES = {
    "default_small": "assets/bulletFire/bulletFireDefaultSmall.png",
    "default_big": "assets/bulletFire/bulletFireDefaultBig.png",
    "long": "assets/bulletFire/bulletFireLong.png",
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
        "fire_img": BULLET_FIRE_IMAGES["default_small"],
        "damage": 10,
        "range": 180,
        "fire_rate": 1.2,
        "bullet_speed": 350,
        "turn_speed": 240,
        "aim_tolerance": 12,
        "barrel_length": 14,
        "cost": 50,
    },

    2: {
            "name": "LongTower",
            "head": "long",
            "head_img": TOWER_HEAD_IMAGES["long"],
            "bullet_img": BULLET_IMAGES["default"],
            "fire_img": BULLET_FIRE_IMAGES["long"],
            "damage": 50,
            "range": 300,
            "fire_rate": 0.5,
            "bullet_speed": 600,
            "turn_speed": 120,
            "aim_tolerance": 12,
            "barrel_length": 14,
            "cost": 100,
        },
}

# BUILDING_DICTIONARY = {
#     1: {"color": "grey", "type": "wall"},
#     2: {"color": "red", "type": "tower"},
# }




# ______________________________________________------------------------------------------------
TILE_ATLAS = {
    'grass_default_1': (0 * tile_size, 6 * tile_size, tile_size, tile_size),
    'grass_default_2': (1 * tile_size, 6 * tile_size, tile_size, tile_size),
    'grass_default_3': (2 * tile_size, 6 * tile_size, tile_size, tile_size),
    'grass_default_4': (3 * tile_size, 6 * tile_size, tile_size, tile_size),

    'water_default': (0 * tile_size, 13 * tile_size, tile_size, tile_size),

    'water_grass_16': (1 * tile_size, 7 * tile_size, tile_size, tile_size), #NW
    'water_grass_32': (2 * tile_size, 7 * tile_size, tile_size, tile_size), #NE
    'water_grass_48': (3 * tile_size, 7 * tile_size, tile_size, tile_size), #NW, NE
    'water_grass_128': (4 * tile_size, 7 * tile_size, tile_size, tile_size), #SE
    'water_grass_144': (5 * tile_size, 7 * tile_size, tile_size, tile_size), #nw, se
    'water_grass_160': (6 * tile_size, 7 * tile_size, tile_size, tile_size), #ne, se
    'water_grass_176': (7 * tile_size, 7 * tile_size, tile_size, tile_size), #ne, se, nw
    'water_grass_64': (0 * tile_size, 8 * tile_size, tile_size, tile_size), #WS
    'water_grass_80': (1 * tile_size, 8 * tile_size, tile_size, tile_size), #NW WS
    'water_grass_96': (2 * tile_size, 8 * tile_size, tile_size, tile_size), #NE WS
    'water_grass_112': (3 * tile_size, 8 * tile_size, tile_size, tile_size), #NW, NE, WS
    'water_grass_192': (4 * tile_size, 8 * tile_size, tile_size, tile_size), #SE WS
    'water_grass_208': (5 * tile_size, 8 * tile_size, tile_size, tile_size), #nw, se, WS
    'water_grass_224': (6 * tile_size, 8 * tile_size, tile_size, tile_size), #ne, se, WS
    'water_grass_240': (7 * tile_size, 8 * tile_size, tile_size, tile_size), #ne, se, nw, NE
    'water_grass_84': (0 * tile_size, 9 * tile_size, tile_size, tile_size), #W
    'water_grass_116': (1 * tile_size, 9 * tile_size, tile_size, tile_size), #W NE
    'water_grass_212': (2 * tile_size, 9 * tile_size, tile_size, tile_size), #W SE
    'water_grass_244': (3 * tile_size, 9 * tile_size, tile_size, tile_size), #W NE SE
    'water_grass_49': (4 * tile_size, 9 * tile_size, tile_size, tile_size), #N
    'water_grass_177': (5 * tile_size, 9 * tile_size, tile_size, tile_size), #N SE
    'water_grass_113': (6 * tile_size, 9 * tile_size, tile_size, tile_size), #N WS
    'water_grass_241': (7 * tile_size, 9 * tile_size, tile_size, tile_size), #N WS SE
    'water_grass_168': (0 * tile_size, 10 * tile_size, tile_size, tile_size), #E
    'water_grass_232': (1 * tile_size, 10 * tile_size, tile_size, tile_size), #E WS
    'water_grass_184': (2 * tile_size, 10 * tile_size, tile_size, tile_size), #E NW
    'water_grass_248': (3 * tile_size, 10 * tile_size, tile_size, tile_size), #E WS NW
    'water_grass_194': (4 * tile_size, 10 * tile_size, tile_size, tile_size), #S
    'water_grass_210': (5 * tile_size, 10 * tile_size, tile_size, tile_size), #S NW
    'water_grass_226': (6 * tile_size, 10 * tile_size, tile_size, tile_size), #S NE
    'water_grass_242': (7 * tile_size, 10 * tile_size, tile_size, tile_size), #S WN SE
    'water_grass_252': (0 * tile_size, 11 * tile_size, tile_size, tile_size), #W E
    'water_grass_243': (1 * tile_size, 11 * tile_size, tile_size, tile_size), #N S
    'water_grass_117': (2 * tile_size, 11 * tile_size, tile_size, tile_size), #W N
    'water_grass_245': (3 * tile_size, 11 * tile_size, tile_size, tile_size), #W N SE
    'water_grass_185': (4 * tile_size, 11 * tile_size, tile_size, tile_size), #N E
    'water_grass_249': (5 * tile_size, 11 * tile_size, tile_size, tile_size), #N E WS
    'water_grass_234': (6 * tile_size, 11 * tile_size, tile_size, tile_size), #S E
    'water_grass_250': (7 * tile_size, 11 * tile_size, tile_size, tile_size), #S E NW
    'water_grass_214': (0 * tile_size, 12 * tile_size, tile_size, tile_size), #W S
    'water_grass_246': (1 * tile_size, 12 * tile_size, tile_size, tile_size), #W S NE
    'water_grass_253': (2 * tile_size, 12 * tile_size, tile_size, tile_size), #W N E
    'water_grass_247': (3 * tile_size, 12 * tile_size, tile_size, tile_size), #N W S
    'water_grass_254': (4 * tile_size, 12 * tile_size, tile_size, tile_size), #W S E
    'water_grass_251': (5 * tile_size, 12 * tile_size, tile_size, tile_size), #N S E
    'water_grass_5':   (2 * tile_size, 11 * tile_size, tile_size, tile_size), # N, W
    'water_grass_1':   (4 * tile_size, 8 * tile_size, tile_size, tile_size), # N
    'water_grass_9':   (4 * tile_size, 11 * tile_size, tile_size, tile_size), # N, E
    'water_grass_4':   (0 * tile_size, 9 * tile_size, tile_size, tile_size), # W
    'water_grass_8':   (0 * tile_size, 10 * tile_size, tile_size, tile_size), # E
    'water_grass_6':   (0 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W
    'water_grass_2':   (4 * tile_size, 10 * tile_size, tile_size, tile_size), # S
    'water_grass_10':  (6 * tile_size, 11 * tile_size, tile_size, tile_size), # S, E
    'water_grass_13':  (2 * tile_size, 12 * tile_size, tile_size, tile_size), # N, W, E
    'water_grass_14':  (4 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, E
    'water_grass_7':   (3 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, W
    'water_grass_11':  (5 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, E
    'water_grass_15':  (6 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, W, E
    'water_grass_21':  (2 * tile_size, 11 * tile_size, tile_size, tile_size), # N, W, NW
    'water_grass_41':  (4 * tile_size, 11 * tile_size, tile_size, tile_size), # N, E, NE
    'water_grass_70':  (0 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, SW
    'water_grass_138': (6 * tile_size, 11 * tile_size, tile_size, tile_size), # S, E, SE
    'water_grass_53':  (2 * tile_size, 11 * tile_size, tile_size, tile_size), # N, W, NW, NE
    'water_grass_57':  (4 * tile_size, 11 * tile_size, tile_size, tile_size), # N, E, NW, NE
    'water_grass_198': (0 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, SW, SE
    'water_grass_202': (6 * tile_size, 11 * tile_size, tile_size, tile_size), # S, E, SW, SE
    'water_grass_87':  (3 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, W, NW, SW
    'water_grass_171': (5 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, E, NE, SE
    'water_grass_61':  (2 * tile_size, 12 * tile_size, tile_size, tile_size), # N, W, E, NW, NE
    'water_grass_206': (4 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, E, SW, SE
    'water_grass_31':  (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW
    'water_grass_47':  (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NE
    'water_grass_79':  (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + SW
    'water_grass_143': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + SE
    'water_grass_63':  (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW, NE
    'water_grass_207': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + SW, SE
    'water_grass_95':  (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW, SW
    'water_grass_175': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NE, SE
    'water_grass_159': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW, SE
    'water_grass_111': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NE, SW
    'water_grass_127': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW, NE, SW
    'water_grass_191': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW, NE, SE
    'water_grass_223': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NW, SW, SE
    'water_grass_239': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + NE, SW, SE
    'water_grass_255': (6 * tile_size, 12 * tile_size, tile_size, tile_size), # 4-cardinal + 4-corner
    'water_grass_85':  (2 * tile_size, 11 * tile_size, tile_size, tile_size), # N, W, NW, SW
    'water_grass_169': (4 * tile_size, 11 * tile_size, tile_size, tile_size), # N, E, NE, SE
    'water_grass_86':  (0 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, NW, SW
    'water_grass_170': (6 * tile_size, 11 * tile_size, tile_size, tile_size), # S, E, NE, SE
    'water_grass_37':  (2 * tile_size, 11 * tile_size, tile_size, tile_size), # N, W, NE
    'water_grass_25':  (4 * tile_size, 11 * tile_size, tile_size, tile_size), # N, E, NW
    'water_grass_134': (0 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, SE
    'water_grass_74':  (6 * tile_size, 11 * tile_size, tile_size, tile_size), # S, E, SW
    'water_grass_151': (3 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, W, NW, SE
    'water_grass_103': (5 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, W, NE, SW
    'water_grass_155': (2 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, E, NW, SE
    'water_grass_107': (4 * tile_size, 12 * tile_size, tile_size, tile_size), # N, S, E, NE, SW
    'water_grass_93':  (3 * tile_size, 12 * tile_size, tile_size, tile_size), # N, W, E, NW, SW
    'water_grass_173': (5 * tile_size, 12 * tile_size, tile_size, tile_size), # N, W, E, NE, SE
    'water_grass_94':  (2 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, E, NW, SW
    'water_grass_174': (4 * tile_size, 12 * tile_size, tile_size, tile_size), # S, W, E, NE, SE
    'water_grass_68': (0 * tile_size, 9 * tile_size, tile_size, tile_size), # W WS
    'water_grass_20': (0 * tile_size, 9 * tile_size, tile_size, tile_size), # W WN
    'water_grass_17': (4 * tile_size, 9 * tile_size, tile_size, tile_size), # N WN
    'water_grass_33': (4 * tile_size, 9 * tile_size, tile_size, tile_size), # N NE
    'water_grass_40': (0 * tile_size, 10 * tile_size, tile_size, tile_size), # E NE
    'water_grass_136': (0 * tile_size, 10 * tile_size, tile_size, tile_size), # E SE
    'water_grass_66': (4 * tile_size, 10 * tile_size, tile_size, tile_size), # S WS
    'water_grass_130': (4 * tile_size, 10 * tile_size, tile_size, tile_size), # S SE
    'water_grass_119': (3 * tile_size, 12 * tile_size, tile_size, tile_size), # N W S WN WS NE
    'water_grass_215': (3 * tile_size, 12 * tile_size, tile_size, tile_size), # N W S WN WS SE
    'water_grass_125': (2 * tile_size, 12 * tile_size, tile_size, tile_size), # W N E WN NE WS
    'water_grass_189': (2 * tile_size, 12 * tile_size, tile_size, tile_size), # W N E WN NE SE
    'water_grass_187': (5 * tile_size, 12 * tile_size, tile_size, tile_size), # N E S NE SE WN
    'water_grass_135': (5 * tile_size, 12 * tile_size, tile_size, tile_size), # N E S NE SE WS
    'water_grass_222': (4 * tile_size, 12 * tile_size, tile_size, tile_size), # W S E WS SE WN
    'water_grass_238': (4 * tile_size, 12 * tile_size, tile_size, tile_size), # W S E WS SE NE
    'water_grass_133': (3 * tile_size, 11 * tile_size, tile_size, tile_size), # W N SE WS
    'water_grass_69': (3 * tile_size, 11 * tile_size, tile_size, tile_size), # W N SE
    'water_grass_213': (3 * tile_size, 11 * tile_size, tile_size, tile_size), # W N WS WN SE
    'water_grass_261': (3 * tile_size, 11 * tile_size, tile_size, tile_size), # W N WS NE SE
    'water_grass_105': (5 * tile_size, 11 * tile_size, tile_size, tile_size), # E N WS NE
    'water_grass_73': (5 * tile_size, 11 * tile_size, tile_size, tile_size), # E N WS
    'water_grass_233': (5 * tile_size, 11 * tile_size, tile_size, tile_size), # E N WS NE SE
    'water_grass_121': (5 * tile_size, 11 * tile_size, tile_size, tile_size), # E N WS NE WN
    'water_grass_26': (7 * tile_size, 11 * tile_size, tile_size, tile_size), # S E WN
    'water_grass_154': (7 * tile_size, 11 * tile_size, tile_size, tile_size), # S E WN SE
    'water_grass_186': (7 * tile_size, 11 * tile_size, tile_size, tile_size), # S E WN SE NE
    'water_grass_218': (7 * tile_size, 11 * tile_size, tile_size, tile_size), # S E WN SE WS
    'water_grass_38': (1 * tile_size, 12 * tile_size, tile_size, tile_size), # W S NE
    'water_grass_102': (1 * tile_size, 12 * tile_size, tile_size, tile_size), # W S NE WS
    'water_grass_118': (1 * tile_size, 12 * tile_size, tile_size, tile_size), # W S NE WS WN
    'water_grass_230': (1 * tile_size, 12 * tile_size, tile_size, tile_size), # W S NE WS SE
}