import pygame

from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece


class Enterprise(GamePiece):
    """Initialize the ship and set its starting position"""

    def __init__(self, screen: pygame.Surface):
        """"""
        super().__init__(screen, 'EnterpriseD.png')

    def update(self, sectorX, sectorY, playTime: float = 0):
        """"""
        super().update(sectorX, sectorY, playTime)
