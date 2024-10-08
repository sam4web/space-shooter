from .settings import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, angle, group):
        super().__init__(group)
        self.original_surf = pygame.image.load(
            join("assets", "images", "bullet.png")
        ).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=pos)

        # movement
        self.speed = 500
        self.direction = pygame.Vector2(direction)
        self.angle = angle

        pygame.mixer.Sound(join("assets", "audio", "bullet.wav")).play()

    def check_collision(self):
        # checks if bullet is out of the display window
        if not (0 <= self.rect.x <= WINDOW_WIDTH and 0 <= self.rect.y <= WINDOW_HEIGHT):
            self.kill()

    def move(self, dt):
        """
        update the bullet's position & rotate the angle according to player's.
        """
        if self.direction.xy == (0, 0):
            self.direction.y = -1
        self.rect.center += self.direction * self.speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.angle, 1)

    def update(self, dt):
        self.move(dt)
        self.check_collision()
