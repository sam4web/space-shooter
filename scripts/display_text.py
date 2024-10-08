from .settings import *


class DisplayText:
    def __init__(
        self, text, size=25, color="#c7dcd0", pos=(0, 0), border=False, padding=(30, 20)
    ):
        self.font = pygame.font.Font(join("assets", "fonts", "Oxanium-Bold.ttf"), size)
        self.surf = self.font.render(text, True, color)
        self.rect = self.surf.get_frect(center=pos)
        self.display_surface = pygame.display.get_surface()
        self.display_surface.blit(self.surf, self.rect)

        if border:
            pygame.draw.rect(
                self.display_surface,
                color,
                self.rect.inflate(padding[0], padding[1]).move(
                    0, (floor(size / 4) * -1)
                ),
                5,
                10,
            )
