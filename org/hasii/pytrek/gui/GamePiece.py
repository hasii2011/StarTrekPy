import pygame

from pygame.sprite import Sprite
from pygame import Surface

from org.hasii.pytrek.Settings import Settings

class GamePiece(Sprite):
    """Provided only to have a common sprite for us to update"""

    QUADRANT_PIXEL_HEIGHT  = 64
    QUADRANT_PIXEL_WIDTH   = 64
    STANDARD_SPRITE_WIDTH  = 32
    STANDARD_SPRITE_HEIGHT = 32
    STANDARD_X_ADJUSTMENT  = (STANDARD_SPRITE_WIDTH / 2)
    STANDARD_Y_ADJUSTMENT  = (STANDARD_SPRITE_WIDTH / 2)


    def __init__(self, screen: Surface, fileNamePath: str):
        """"""
        super().__init__()

        self.screen          = screen
        self.settings        = Settings()
        self.image           = pygame.image.load(fileNamePath)
        self.currentPosition = None
        self.playTime        = 0.0
        #
        #
        self.rect   = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x      = float(self.rect.x)

    def update(self, sectorX: int, sectorY: int, playTime: float = 0):
        """"""

        self.rect.x = ((sectorX * GamePiece.STANDARD_SPRITE_WIDTH)  * 2) + GamePiece.STANDARD_X_ADJUSTMENT + self.settings.leftMargin
        self.rect.y = ((sectorY * GamePiece.STANDARD_SPRITE_HEIGHT) * 2) + GamePiece.STANDARD_Y_ADJUSTMENT

        # print("sectorX: " + str(sectorX) + " self.rect.x: " + str(self.rect.x) + " sectorY: " + str(sectorY) + " self.rect.y: " +str(self.rect.y))
        # print(str(self.rect))
        self.screen.blit(self.image, self.rect)
