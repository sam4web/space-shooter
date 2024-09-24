import pygame


class SpriteAnimation(pygame.sprite.Sprite):
    def __init__(self, frames, pos, group):
        super().__init__(group)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)
        self.animation_speed = 50

    def update(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
