import pygame


class Bullet(pygame.sprite.Sprite):
    """Projectile flying at a target building, deals damage on impact."""

    def __init__(self, pos, target, damage, speed, radius=3, color="white"):
        super().__init__()
        self.pos = pygame.Vector2(pos)  # position in world space
        self.target = target
        self.damage = damage
        self.speed = speed  # world px/s
        self.radius = radius
        self.color = color

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
        self.pos += direction.normalize() * step

    def draw(self, screen, camera):
        center = camera.world_to_screen(self.pos.x, self.pos.y)
        pygame.draw.circle(screen, self.color, center, max(1, round(self.radius * camera.zoom)))
