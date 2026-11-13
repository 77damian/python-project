import random

import pygame

from bullet import Bullet
from constants import *

class Enemy(pygame.sprite.Sprite):
    """Walks to its target building and attacks it once in range.

    Subclasses define the stats:
    color, radius (collision circle, world px), damage, speed (world px/s),
    attack_range (world px, edge to edge), attack_cooldown (s), spawn_weight.
    """

    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)  # position in world space
        self.target = None
        self.cooldown_left = 0.0

        # placeholder graphics
        size = self.radius * 2
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(round(x), round(y)))

    def set_target(self, building):
        self.target = building

    def update(self, dt, bullets):
        self.cooldown_left = max(0.0, self.cooldown_left - dt)
        if self.target is None or not self.target.alive():
            return

        distance_left = self.target.distance_to(self.pos) - self.radius - self.attack_range
        if distance_left > RANGE_TOLERANCE:
            self.move_to_target(min(self.speed * dt, distance_left))
        elif self.cooldown_left == 0:
            self.attack(bullets)
            self.cooldown_left = self.attack_cooldown

    def move_to_target(self, step):
        direction = pygame.Vector2(self.target.rect.center) - self.pos
        self.pos += direction.normalize() * step
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    # melee by default, ranged enemies override this
    def attack(self, bullets):
        self.target.take_damage(self.damage)

    # enemies draw themselves
    def draw(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)
        screen.blit(pygame.transform.scale(self.image, screen_rect.size), screen_rect)


class Warrior(Enemy):
    color = "red"
    radius = 12
    damage = 10
    speed = 60
    attack_range = 4
    attack_cooldown = 1.0
    spawn_weight = 6


class Tank(Enemy):
    color = "navy"
    radius = 24
    damage = 40
    speed = 30
    attack_range = 4
    attack_cooldown = 2.0
    spawn_weight = 1


class Archer(Enemy):
    color = "yellow"
    radius = 10
    damage = 6
    speed = 70
    attack_range = 180
    attack_cooldown = 1.5
    spawn_weight = 3
    bullet_speed = 300

    def attack(self, bullets):
        bullets.add(Bullet(self.pos, self.target, self.damage, self.bullet_speed))


ENEMY_TYPES = (Warrior, Tank, Archer)


# random enemy type on the border of the world, heading for the target building
def spawn_enemy(target):
    weights = [enemy_type.spawn_weight for enemy_type in ENEMY_TYPES]
    enemy_type = random.choices(ENEMY_TYPES, weights=weights)[0]
    enemy = enemy_type(*random_edge_position())
    enemy.set_target(target)
    return enemy


# random point on the border of the world
def random_edge_position():
    side = random.choice("NSWE")
    if side == "N":
        return random.uniform(0, WORLD_WIDTH), 0
    if side == "S":
        return random.uniform(0, WORLD_WIDTH), WORLD_HEIGHT
    if side == "W":
        return 0, random.uniform(0, WORLD_HEIGHT)
    return WORLD_WIDTH, random.uniform(0, WORLD_HEIGHT)
