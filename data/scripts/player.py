import os

import pygame

from .settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.group = group
        self.original_surf = pygame.image.load(
            os.path.join("data", "images", "ship.png")
        ).convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # movement
        self.direction = pygame.Vector2()
        self.speed = 350
        self.angle = 0

        # bullet
        self.can_shoot = True
        self.last_shot_time = 0
        self.cooldown_durations = 250

    def check_diagonal_movement(self):
        """
        check diagonal movement and set angle accordingly
        """
        if self.direction.x != 0 and self.direction.y != 0:
            # up-right
            if self.direction.x > 0 > self.direction.y:
                self.angle = -45
            # up-left
            elif self.direction.x < 0 and self.direction.y < 0:
                self.angle = 45
            # down-right
            elif self.direction.x > 0 and self.direction.y > 0:
                self.angle = -135
            # down-left
            elif self.direction.x < 0 < self.direction.y:
                self.angle = 135

    def bullet_timer(self):
        """
        cooldown time to determine if the player can shoot a bullet.
        """
        if self.can_shoot:
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.cooldown_durations:
            self.can_shoot = True

    def shoot_bullet(self):
        """
        tracks last shot time.
        """
        self.last_shot_time = pygame.time.get_ticks()
        self.can_shoot = False
        self.check_diagonal_movement()

    def input(self):
        """
        handles player input for movement, setting direction and angle.
        """
        keys = pygame.key.get_pressed()
        # handle horizontal movement
        if keys[pygame.K_LEFT] and self.rect.left >= 0:
            self.direction.x = -1
            self.angle = 90
        elif keys[pygame.K_RIGHT] and self.rect.right <= WINDOW_WIDTH:
            self.direction.x = 1
            self.angle = -90
        else:
            self.direction.x = 0

        # handle vertical movement
        if keys[pygame.K_DOWN] and self.rect.bottom <= WINDOW_HEIGHT:
            self.direction.y = 1
            self.angle = 180
        elif keys[pygame.K_UP] and self.rect.top >= 0:
            self.direction.y = -1
            self.angle = 0
        else:
            self.direction.y = 0

        # check for diagonal movement and set the correct angle
        self.check_diagonal_movement()

        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )

    def move(self, dt):
        """
        update the player's position and angle
        """
        self.rect.center += self.direction * self.speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.angle, 1)

    def update(self, dt):
        self.bullet_timer()
        self.input()
        self.move(dt)
