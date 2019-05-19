import pygame

from org.hasii.pytrek.gui.GamePiece import GamePiece

class Enterprise(GamePiece):
    """Initialize the ship and set its starting position"""

    def __init__(self, screen: pygame.Surface):
        """"""
        super().__init__(screen, 'images/EnterpriseD.png')


    def update(self, sectorX, sectorY):
        """"""
        super().update(sectorX, sectorY)
