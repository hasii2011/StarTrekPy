
import pygame

from pygame import Surface

from pygame.sprite import Sprite


class BaseBackGround(Sprite):

    def __init__(self, screen: Surface, fileName: str):

        super().__init__()

        self.screen: Surface = screen
        self.image = pygame.image.load(fileName)

        self.rect   = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x      = float(self.rect.x)

    def update(self, *args):
        pass
