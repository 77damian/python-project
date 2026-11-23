import math
import pygame
from constants import SPRITE_ANGLE_OFFSET


class Bullet(pygame.sprite.Sprite):
    """Projectile flying at a target, deals damage on impact."""

    def __init__(self, pos, target, damage, speed, radius=3, color="white", image=None, angle=0.0):
        super().__init__()
        self.pos = pygame.Vector2(pos)  # position in world space
        self.target = target
        self.damage = damage
        self.speed = speed  # world px/s
        self.radius = radius
        self.color = color
        self.image = image
        self.angle = angle

    def update(self, dt):
        if not self.target.alive():
            self.kill()
            return

        step = self.speed * dt
        if self.target.distance_to(self.pos) - self.radius <= step:
            self.target.take_damage(self.damage)
            self.kill()
            return

        direction = pygame.Vector2(self.target.rect.center) - self.pos
        if direction.length_squared() > 0:
            self.angle = -math.degrees(math.atan2(direction.y, direction.x))
            self.pos += direction.normalize() * step

    def draw(self, screen, camera):
        center = camera.world_to_screen(self.pos.x, self.pos.y)
        if self.image is not None:
            scaled_size = (
                max(0.5, round(self.image.get_width() * camera.zoom)),
                max(0.5, round(self.image.get_height() * camera.zoom)),
            )
            scaled_img = pygame.transform.scale(self.image, scaled_size)
            rotated_img = pygame.transform.rotate(scaled_img, self.angle + SPRITE_ANGLE_OFFSET)
            rect = rotated_img.get_rect(center=(round(center[0]), round(center[1])))
            screen.blit(rotated_img, rect)
        else:
            pygame.draw.circle(screen, self.color, center, max(1, round(self.radius * camera.zoom)))


class RocketBullet(Bullet):
    """Rocket projectile that explodes on impact, dealing circular AoE damage."""

    def __init__(self, pos, target, damage, speed, splash_radius, enemies, image=None, angle=0.0):
        super().__init__(pos, target, damage, speed, image=image, angle=angle)
        self.splash_radius = splash_radius
        self.enemies = enemies
        self.target_pos = pygame.Vector2(target.rect.center)

        self.exploding = False
        self.explosion_duration = 0.2
        self.explosion_timer = 0.0

    def explode(self):
        for enemy in self.enemies:
            if enemy.alive() and enemy.distance_to(self.pos) <= self.splash_radius:
                enemy.take_damage(self.damage)

        self.exploding = True
        self.explosion_timer = self.explosion_duration

    def update(self, dt):
        if self.exploding:
            self.explosion_timer -= dt
            if self.explosion_timer <= 0.0:
                self.kill()
            return

        if self.target.alive():
            self.target_pos = pygame.Vector2(self.target.rect.center)

        to_target = self.target_pos - self.pos
        step = self.speed * dt

        if to_target.length() <= step:
            self.pos = self.target_pos
            self.explode()
            return

        self.angle = -math.degrees(math.atan2(to_target.y, to_target.x))
        self.pos += to_target.normalize() * step

    def draw(self, screen, camera):
        if not self.exploding:
            super().draw(screen, camera)
            return

        progress = 1.0 - (self.explosion_timer / self.explosion_duration)
        world_radius = self.splash_radius * progress
        screen_radius = max(1, round(world_radius * camera.zoom))
        fade = 1.0 - progress

        diameter = screen_radius * 2
        surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 140, 40, int(90 * fade)), (screen_radius, screen_radius), screen_radius)
        pygame.draw.circle(surface, (255, 210, 90, int(220 * fade)), (screen_radius, screen_radius), screen_radius, 2)

        center = camera.world_to_screen(self.pos.x, self.pos.y)
        rect = surface.get_rect(center=(round(center[0]), round(center[1])))
        screen.blit(surface, rect)