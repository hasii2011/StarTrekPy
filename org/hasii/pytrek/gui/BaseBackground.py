
import pygame

from pygame import Surface

from pygame.sprite import Sprite

from org.hasii.pytrek.Settings import Settings


class BaseBackGround(Sprite):

    def __init__(self, screen: Surface, fileName: str):

        super().__init__()

        self.screen: Surface = screen

        fqFileName: str = Settings.getResourcesPath(bareFileName=fileName,
                                                    resourcePackageName=Settings.IMAGE_RESOURCES_PACKAGE_NAME,
                                                    resourcesPath=Settings.IMAGE_RESOURCES_PATH
                                                    )

        self.image = pygame.image.load(fqFileName)

        self.rect   = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x      = float(self.rect.x)

    def update(self, *args):
        pass
