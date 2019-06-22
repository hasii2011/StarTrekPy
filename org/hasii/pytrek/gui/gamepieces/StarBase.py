import pygame

from org.hasii.pytrek.gui.GamePiece import GamePiece


class StarBase(GamePiece):
    """"""
    def __init__(self, screen: pygame.Surface):
        """"""
        super().__init__(screen, 'images/StarBase3.png')

    def update(self, sectorX, sectorY, playTime: float = 0):
        """"""
        super().update(sectorX, sectorY, playTime)
