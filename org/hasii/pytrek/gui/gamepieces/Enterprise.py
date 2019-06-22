import pygame

from hasii.pytrek.gui.gamepieces.GamePiece import GamePiece


class Enterprise(GamePiece):
    """Initialize the ship and set its starting position"""

    def __init__(self, screen: pygame.Surface):
        """"""
        super().__init__(screen, 'images/EnterpriseD.png')


    def update(self, sectorX, sectorY, playTime: float):
        """"""
        super().update(sectorX, sectorY, playTime)
