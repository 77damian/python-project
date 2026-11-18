import math
import pygame

from building.building import Building
from bullet import DefaultBullet
from constants import TOWER_BASE_IMAGES, TOWERS_DATA


class Tower(Building):
    _image_cache = {}

    def __init__(self, world_x, world_y, tower_id=1):
        super().__init__(world_x, world_y)
        self.tower_id = tower_id
        self.level = 1

        data = TOWERS_DATA[tower_id]
        self.name = data["name"]
        self.head = data["head"]
        self.damage = data["damage"]
        self.range = data["range"]
        self.fire_rate = data["fire_rate"]
        self.bullet_speed = data["bullet_speed"]
        self.cost = data["cost"]

        self.base_img = self._load_image(TOWER_BASE_IMAGES[self.level])
        self.head_img = self._load_image(data["head_img"])
        self.bullet_img = self._load_image(data["bullet_img"])

        self.img = {
            "base": self.base_img,
            "head": self.head_img,
            "bullet": self.bullet_img,
        }

        self.angle = 0.0
        self.shoot_timer = 0.0
        self.target = None
        self.bullets = pygame.sprite.Group()

    @classmethod
    def _load_image(cls, path):
        if path not in cls._image_cache:
            cls._image_cache[path] = pygame.image.load(path).convert_alpha()
        return cls._image_cache[path]

    def find_target(self, enemies):
        tower_center = pygame.Vector2(self.rect.center)
        closest_enemy = None
        closest_dist = self.range

        for enemy in enemies:
            if not enemy.alive():
                continue
            dist = tower_center.distance_to(enemy.pos)
            if dist <= closest_dist:
                closest_dist = dist
                closest_enemy = enemy

        self.target = closest_enemy
        return self.target

    def shoot(self, target):
        bullet = DefaultBullet(
            x=self.rect.centerx,
            y=self.rect.centery,
            target=target,
            image=self.bullet_img,
            speed=self.bullet_speed,
            damage=self.damage,
        )
        self.bullets.add(bullet)

    def update(self, dt, enemies=None):
        super().update(dt)

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

        if enemies is not None:
            target = self.find_target(enemies)
            if target is not None:
                direction = target.pos - pygame.Vector2(self.rect.center)
                self.angle = -math.degrees(math.atan2(direction.y, direction.x))

                if self.shoot_timer <= 0:
                    self.shoot(target)
                    self.shoot_timer = 1.0 / self.fire_rate

        self.bullets.update(dt)

    def draw(self, screen, camera):
        pass


class BaseTower(Tower):
    ID = 1

    def __init__(self, world_x, world_y):
        super().__init__(world_x, world_y, tower_id=self.ID)

    def draw(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)

        scaled_base = pygame.transform.scale(self.base_img, screen_rect.size)
        screen.blit(scaled_base, screen_rect)

        scale_x = screen_rect.width / self.base_img.get_width()
        scale_y = screen_rect.height / self.base_img.get_height()
        head_size = (
            round(self.head_img.get_width() * scale_x),
            round(self.head_img.get_height() * scale_y),
        )
        scaled_head = pygame.transform.scale(self.head_img, head_size)
        rotated_head = pygame.transform.rotate(scaled_head, self.angle)
        head_rect = rotated_head.get_rect(center=screen_rect.center)
        screen.blit(rotated_head, head_rect)

        for bullet in self.bullets:
            bullet.draw(screen, camera)

    def draw_preview(self, screen, camera):
        screen_rect = camera.world_rect_to_screen(self.rect)

        preview_base = pygame.transform.scale(self.base_img, screen_rect.size)
        preview_base.set_alpha(150)
        screen.blit(preview_base, screen_rect)

        scale_x = screen_rect.width / self.base_img.get_width()
        scale_y = screen_rect.height / self.base_img.get_height()
        head_size = (
            round(self.head_img.get_width() * scale_x),
            round(self.head_img.get_height() * scale_y),
        )
        preview_head = pygame.transform.scale(self.head_img, head_size)
        preview_head.set_alpha(150)
        head_rect = preview_head.get_rect(center=screen_rect.center)
        screen.blit(preview_head, head_rect)