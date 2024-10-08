from random import randrange, uniform

from .settings import *


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.original_surf = pygame.image.load(
            join("data", "images", "asteroid.png")
        ).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(randrange(WINDOW_WIDTH), -10))

        # movement
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), uniform(0.5, 1))
        self.speed = randrange(450, 700)

        # rotation
        self.rotation = 0
        self.rotation_speed = randrange(40, 80)

        # countdown
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000

    def asteroid_timer(self):
        current_time = pygame.time.get_ticks()
        if (current_time - self.start_time) >= self.life_time:
            self.kill()

    def move(self, dt):
        self.rotation += dt * self.rotation_speed
        self.rect.center += self.direction * self.speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)

    def update(self, dt):
        self.asteroid_timer()
        self.move(dt)
