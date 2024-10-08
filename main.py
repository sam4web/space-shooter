import pygame.time

from scripts.asteroid import Asteroid
from scripts.bullet import Bullet
from scripts.display_text import DisplayText
from scripts.player import Player
from scripts.settings import *
from scripts.sprite_animation import SpriteAnimation


class Game:

    def __init__(self):
        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load(
            join("data", "images", "space-bg.jpg")
        ).convert_alpha()
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_game()

        # astroid timer
        self.asteroid_cooldown = 150
        self.last_asteroid_summon_time = 0

        # group
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.asteroid_sprites = pygame.sprite.Group()

        # sprites
        self.player = Player(self.all_sprites)

        # frames
        self.explosion_frames = [
            pygame.image.load(
                join("data", "images", "explosion", f"{i}.png")
            ).convert_alpha()
            for i in range(7)
        ]

        # game music
        game_music = pygame.mixer.Sound(join("data", "audio", "game_music.wav"))
        game_music.set_volume(0.4)
        game_music.play()

    def display_score(self):
        # score
        DisplayText(
            text="Score: " + (f"0{self.score}" if self.score < 10 else str(self.score)),
            size=35,
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 70),
            border=True,
        )
        # high score
        DisplayText(
            text=f"High Score: {self.high_score}",
            pos=(110, 35),
        )

    def asteroid_timer(self):
        """
        tracks the time since the last asteroid summon and spawns a new one if the cooldown has passed.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_asteroid_summon_time >= self.asteroid_cooldown:
            self.last_asteroid_summon_time = pygame.time.get_ticks()
            Asteroid((self.all_sprites, self.asteroid_sprites))

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
                self.update_score()
                # explosion sound & animation
                pygame.mixer.Sound(join("data", "audio", "explosion.wav")).play()
                SpriteAnimation(
                    self.explosion_frames, bullet.rect.midtop, self.all_sprites
                )

        # check for player collision
        if pygame.sprite.spritecollide(
            self.player, self.asteroid_sprites, False, pygame.sprite.collide_mask
        ):
            self.reset_game()

    def update_score(self):
        self.score += floor(10 * uniform(0, 1) + uniform(0, 10))

    def get_high_score(self):
        """
        imports the high score from file and loads it into the game
        """
        try:
            with open(score_file, "r") as file:
                self.high_score = json.load(file)["highScore"]
        except:
            self.high_score = 0

    def check_score(self):
        """
        updates the file with the new high score if the current score exceeds the previous high score
        """
        if self.score > self.high_score:
            with open(score_file, "w") as file:
                self.high_score = self.score
                json.dump({"highScore": self.high_score}, file)

    def load_game(self):
        self.get_high_score()
        self.score = 0

    def clear_screen(self):
        """
        clears asteroids and bullets sprites from display screen
        """
        for sprite in self.asteroid_sprites:
            sprite.kill()
        for sprite in self.bullet_sprites:
            sprite.kill()

    def reset_game(self):
        """
        resets the game by updating the high score, resetting the score, and clearing asteroids and bullets.
        """
        self.check_score()
        self.load_game()
        self.player.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.clear_screen()

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
            self.check_collision()
            self.asteroid_timer()
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
