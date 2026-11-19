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
                max(1, round(self.image.get_width() * camera.zoom)),
                max(1, round(self.image.get_height() * camera.zoom)),
            )
            scaled_img = pygame.transform.scale(self.image, scaled_size)
            rotated_img = pygame.transform.rotate(scaled_img, self.angle + SPRITE_ANGLE_OFFSET)
            rect = rotated_img.get_rect(center=(round(center[0]), round(center[1])))
            screen.blit(rotated_img, rect)
        else:
            pygame.draw.circle(screen, self.color, center, max(1, round(self.radius * camera.zoom)))