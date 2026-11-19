import math
import pygame

from building.building import Building
from bullet import Bullet
from constants import *


class Tower(Building):
    _image_cache = {}

    def __init__(self, world_x, world_y, tower_id=1):
        super().__init__(world_x, world_y)
        self.tower_id = tower_id
        self.level = 1  # wieża zawsze zaczyna na poziomie 1

        data = TOWERS_DATA[tower_id]
        self.name = data["name"]
        self.head = data["head"]
        self.damage = data["damage"]
        self.range = data["range"]
        self.fire_rate = data["fire_rate"]
        self.bullet_speed = data["bullet_speed"]
        self.turn_speed = data["turn_speed"]
        self.aim_tolerance = data["aim_tolerance"]
        self.barrel_length = data["barrel_length"]
        self.cost = data["cost"]

        self.base_img = self._load_image(TOWER_BASE_IMAGES[self.level])
        self.head_img = self._load_image(data["head_img"])
        self.bullet_img = self._load_image(data["bullet_img"])
        self.fire_img = self._load_image(data["fire_img"])

        self.img = {
            "base": self.base_img,
            "head": self.head_img,
            "bullet": self.bullet_img,
            "fire": self.fire_img,
        }

        self.angle = 90.0
        self.shoot_timer = 0.0
        self.muzzle_flash_timer = 0.0
        self.target = None

    @classmethod
    def _load_image(cls, path):
        if path not in cls._image_cache:
            cls._image_cache[path] = pygame.image.load(path).convert_alpha()
        return cls._image_cache[path]

    def get_forward_vector(self):
        rad = math.radians(self.angle)
        return pygame.Vector2(math.cos(rad), -math.sin(rad))

    def get_muzzle_pos(self):
        center = pygame.Vector2(self.rect.center)
        return center + self.get_forward_vector() * self.barrel_length

    def find_target(self, enemies):
        if self.target is not None and self.target.alive():
            if self.target.distance_to(self.rect.center) <= self.range:
                return self.target

        closest_enemy = None
        closest_dist = self.range

        for enemy in enemies:
            if not enemy.alive():
                continue
            dist = enemy.distance_to(self.rect.center)
            if dist <= closest_dist:
                closest_dist = dist
                closest_enemy = enemy

        self.target = closest_enemy
        return self.target

    def rotate_towards(self, target_pos, dt):
        dx = target_pos.x - self.rect.centerx
        dy = target_pos.y - self.rect.centery
        desired_angle = -math.degrees(math.atan2(dy, dx))

        # Najkrótsza różnica kątowa w zakresie [-180, 180]
        angle_diff = (desired_angle - self.angle + 180.0) % 360.0 - 180.0
        max_step = self.turn_speed * dt

        if abs(angle_diff) <= max_step:
            self.angle = desired_angle
        else:
            self.angle += math.copysign(max_step, angle_diff)

        self.angle = (self.angle + 180.0) % 360.0 - 180.0
        return abs((desired_angle - self.angle + 180.0) % 360.0 - 180.0)

    def shoot(self, target, bullets):
        bullet = Bullet(
            pos=self.rect.center,
            target=target,
            damage=self.damage,
            speed=self.bullet_speed,
            image=self.bullet_img,
        )
        bullets.add(bullet)
        self.muzzle_flash_timer = 0.06

    def update(self, dt, enemies=None, bullets=None):
        super().update(dt)

        if self.shoot_timer > 0.0:
            self.shoot_timer -= dt
        if self.muzzle_flash_timer > 0.0:
            self.muzzle_flash_timer -= dt

        if enemies is None or bullets is None:
            return
        target = self.find_target(enemies)
        if target is None:
            return

        angle_error = self.rotate_towards(target.pos, dt)

        if angle_error <= self.aim_tolerance and self.shoot_timer <= 0.0:
            self.shoot(target, bullets)
            self.shoot_timer = 1.0 / self.fire_rate

    def draw(self, screen, camera):
        pass


class BaseTower(Tower):
    ID = 1

    def __init__(self, world_x, world_y):
        super().__init__(world_x, world_y, tower_id=self.ID)

    def _blit_rotated_part(self, screen, camera, image, world_center, screen_scale_x, screen_scale_y, alpha=255):
        size = (
            max(1, round(image.get_width() * screen_scale_x)),
            max(1, round(image.get_height() * screen_scale_y)),
        )
        scaled = pygame.transform.scale(image, size)
        if alpha < 255:
            scaled.set_alpha(alpha)
        rotated = pygame.transform.rotate(scaled, self.angle + SPRITE_ANGLE_OFFSET)
        screen_center = camera.world_to_screen(world_center[0], world_center[1])
        rect = rotated.get_rect(center=(round(screen_center[0]), round(screen_center[1])))
        screen.blit(rotated, rect)

    def draw(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)
        scale_x = screen_rect.width / self.base_img.get_width()
        scale_y = screen_rect.height / self.base_img.get_height()

        # 1. Baza lvl 1 (towerBaseLvl1.png)
        scaled_base = pygame.transform.scale(self.base_img, screen_rect.size)
        screen.blit(scaled_base, screen_rect)

        # 2. Błysk wystrzału na końcu lufy (bulletFireDefaultSmall.png)
        if self.muzzle_flash_timer > 0.0:
            muzzle_pos = self.get_muzzle_pos()
            self._blit_rotated_part(screen, camera, self.fire_img, muzzle_pos, scale_x, scale_y)

        # 3. Obrócona głowica default (towerHeadDefault.png)
        self._blit_rotated_part(screen, camera, self.head_img, self.rect.center, scale_x, scale_y)

    def draw_preview(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)
        scale_x = screen_rect.width / self.base_img.get_width()
        scale_y = screen_rect.height / self.base_img.get_height()

        preview_base = pygame.transform.scale(self.base_img, screen_rect.size)
        preview_base.set_alpha(150)
        screen.blit(preview_base, screen_rect)

        self._blit_rotated_part(screen, camera, self.head_img, self.rect.center, scale_x, scale_y, alpha=150)


class LongTower(Tower):
    ID = 2

    def __init__(self, world_x, world_y):
        super().__init__(world_x, world_y, tower_id=self.ID)

    def _blit_rotated_part(self, screen, camera, image, world_center, screen_scale_x, screen_scale_y, alpha=255):
        size = (
            max(1, round(image.get_width() * screen_scale_x)),
            max(1, round(image.get_height() * screen_scale_y)),
        )
        scaled = pygame.transform.scale(image, size)
        if alpha < 255:
            scaled.set_alpha(alpha)
        rotated = pygame.transform.rotate(scaled, self.angle + SPRITE_ANGLE_OFFSET)
        screen_center = camera.world_to_screen(world_center[0], world_center[1])
        rect = rotated.get_rect(center=(round(screen_center[0]), round(screen_center[1])))
        screen.blit(rotated, rect)

    def draw(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)
        scale_x = screen_rect.width / self.base_img.get_width()
        scale_y = screen_rect.height / self.base_img.get_height()

        # 1. Baza lvl 1 (towerBaseLvl1.png)
        scaled_base = pygame.transform.scale(self.base_img, screen_rect.size)
        screen.blit(scaled_base, screen_rect)

        # 2. Błysk wystrzału na końcu lufy (bulletFireDefaultSmall.png)
        if self.muzzle_flash_timer > 0.0:
            muzzle_pos = self.get_muzzle_pos()
            self._blit_rotated_part(screen, camera, self.fire_img, muzzle_pos, scale_x, scale_y)

        # 3. Obrócona głowica default (towerHeadDefault.png)
        self._blit_rotated_part(screen, camera, self.head_img, self.rect.center, scale_x, scale_y)

    def draw_preview(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)
        scale_x = screen_rect.width / self.base_img.get_width()
        scale_y = screen_rect.height / self.base_img.get_height()

        preview_base = pygame.transform.scale(self.base_img, screen_rect.size)
        preview_base.set_alpha(150)
        screen.blit(preview_base, screen_rect)

        self._blit_rotated_part(screen, camera, self.head_img, self.rect.center, scale_x, scale_y, alpha=150)