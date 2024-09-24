import os.path
import sys

import pygame

from data.scripts.asteroid import Asteroid
from data.scripts.bulllet import Bullet
from data.scripts.player import Player
from data.scripts.settings import *
from data.scripts.sprite_animation import SpriteAnimation


class Game:

    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load(
            os.path.join("data", "images", "space-bg.jpg")
        ).convert_alpha()
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.asteroid_summon_cooldown = 200
        self.last_asteroid_summon_time = 0
        self.current_level = 0
        self.asteroid_destroyed = 0

        # group
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player(self.all_sprites)

        # frames
        self.explosion_frames = [
            pygame.image.load(
                os.path.join("data", "images", "explosion", f"{i}.png")
            ).convert_alpha()
            for i in range(7)
        ]

        # game music
        game_music = pygame.mixer.Sound(os.path.join("data", "audio", "game_music.wav"))
        game_music.set_volume(0.4)
        game_music.play()

    def display_score(self):
        font = pygame.font.Font(os.path.join("data", "fonts", "Oxanium-Bold.ttf"), 35)
        score = self.asteroid_destroyed * (self.current_level + 10)
        score = "Score: " + (f"0{score}" if score < 10 else str(score))
        text_surf = font.render(score, True, "#c7dcd0")
        text_rect = text_surf.get_frect(
            midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50)
        )
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface,
            "#c7dcd0",
            text_rect.inflate(30, 20).move(0, -8),
            5,
            10,
        )

    def difficulty_timer(self):
        """
        Checks the time since the game started and decreases asteroid cooldown when it matches the level's time step.
        """
        levels_time_stamp = [8, 14, 18, 22]
        current_time = pygame.time.get_ticks() // 1000 + 1

        if self.current_level >= len(levels_time_stamp):
            self.asteroid_summon_cooldown = 0
            return

        if current_time >= levels_time_stamp[self.current_level]:
            self.current_level += 1
            self.asteroid_summon_cooldown -= 50

    def check_collision(self):
        """
        checks if the asteroid collides with a bullet or player. Destroys the asteroid if hit by a bullet,
        stops the game if it hits the player.
        """

        # check for bullet collision
        for bullet in self.bullet_sprites:
            collided_sprites = pygame.sprite.spritecollide(
                bullet, self.asteroid_sprites, True, pygame.sprite.collide_mask
            )
            if collided_sprites:
                bullet.kill()
                self.asteroid_destroyed += 1
                # explosion sound & animation
                pygame.mixer.Sound(
                    os.path.join("data", "audio", "explosion.wav")
                ).play()
                SpriteAnimation(
                    self.explosion_frames, bullet.rect.midtop, self.all_sprites
                )

        # check for player collision
        if pygame.sprite.spritecollide(
            self.player, self.asteroid_sprites, False, pygame.sprite.collide_mask
        ):
            self.running = False

    def asteroid_timer(self):
        """
        tracks the time since the last asteroid summon and spawns a new one if the cooldown has passed.
        """
        current_time = pygame.time.get_ticks()
        if (
            current_time - self.last_asteroid_summon_time
            >= self.asteroid_summon_cooldown
        ):
            self.last_asteroid_summon_time = pygame.time.get_ticks()
            Asteroid((self.all_sprites, self.asteroid_sprites))

    def shoot_bullet(self):
        """
        tracks last shot time and creates Bullet object.
        """
        self.player.shoot_bullet()
        Bullet(
            pos=self.player.rect.center,
            direction=self.player.direction,
            angle=self.player.angle,
            group=(self.bullet_sprites, self.all_sprites),
        )

    def input(self):
        """
        triggers bullet shooting when space-bar is pressed.
        """
        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.player.can_shoot:
            self.shoot_bullet()

        self.player.angle = 0

    def run(self):
        while self.running:
            # delta time
            dt = self.clock.tick() / 1000

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    self.running = False

            # update
            self.input()
            self.asteroid_timer()
            self.check_collision()
            self.difficulty_timer()
            self.all_sprites.update(dt)

            # draw
            self.display_surface.blit(self.background, (0, 0))
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
