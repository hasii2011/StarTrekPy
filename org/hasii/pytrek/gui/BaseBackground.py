
import pygame
from pkg_resources import resource_filename

from pygame import Surface

from pygame.sprite import Sprite

from org.hasii.pytrek.Settings import Settings


class BaseBackGround(Sprite):

    def __init__(self, screen: Surface, fileName: str):

        super().__init__()

        self.screen: Surface = screen
        fqFileName = resource_filename(Settings.IMAGE_RESOURCES_PACKAGE_NAME, fileName)

        self.image = pygame.image.load(fqFileName)

        self.rect   = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x      = float(self.rect.x)

    def update(self, *args):
        pass
