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
        self.image.fill(Color("#435464"))
        self.rect = Rect(x, y, width, height)

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y, width, height):
        Platform.__init__(self, x, y, width, height)
        self.image.fill(Color("#FFFFCC"))


class DeathBlock(Platform):
    def __init__(self, x, y, width, height):
        Platform.__init__(self, x, y, width, height)
        self.image.fill(Color("#FF0000"))


