import pygame
from pygame import *


class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Platform(Entity):
    def __init__(self, x, y, width, height):
        Entity.__init__(self)
        self.image = Surface((width, height))
        self.image.convert()
        # self.image.fill(Color("#435464"))
        self.image = pygame.image.load("blokido_sprites\platform.png").convert()
        # self.rect = self.image.get_rect()
        self.rect = Rect(x, y, width, height)

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y, width, height):
        Platform.__init__(self, x, y, width, height)
        self.image = pygame.image.load("blokido_sprites\end_message.png").convert()


class DeathBlock(Platform):
    def __init__(self, x, y, width, height):
        Platform.__init__(self, x, y, width, height)
        self.image = pygame.image.load("blokido_sprites\deathblock.png").convert()


