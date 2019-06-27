
from typing import cast

import pygame

from pygame.sprite import Sprite
from pygame import Surface

from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.objects.Coordinates import Coordinates


class GamePiece(Sprite):
    """Provided only to have a common sprite for us to update"""

    QUADRANT_PIXEL_HEIGHT  = 64
    QUADRANT_PIXEL_WIDTH   = 64
    STANDARD_SPRITE_WIDTH  = 32
    STANDARD_SPRITE_HEIGHT = 32
    MEDIUM_SPRITE_WIDTH    = 16
    MEDIUM_SPRITE_HEIGHT   = 16
    STANDARD_X_ADJUSTMENT  = (STANDARD_SPRITE_WIDTH / 2)
    STANDARD_Y_ADJUSTMENT  = (STANDARD_SPRITE_WIDTH / 2)
    MEDIUM_X_ADJUSTMENT    = MEDIUM_SPRITE_WIDTH
    MEDIUM_Y_ADJUSTMENT    = MEDIUM_SPRITE_WIDTH

    def __init__(self, screen: Surface, fileNamePath: str):
        """"""
        super().__init__()

        self.screen:   Surface  = screen
        self.image:    Surface  = pygame.image.load(fileNamePath)
        self.settings: Settings = Settings()
        self.playTime: float    = 0.0

        self.currentPosition: Coordinates = cast(Coordinates, None)

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

        # print(f"sectorX: {str(sectorX)} self.rect.x: {str(self.rect.x)} sectorY: {str(sectorY)} self.rect.y: {str(self.rect.y)}")
        # print(str(self.rect))
        self.screen.blit(self.image, self.rect)

