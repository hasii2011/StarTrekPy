import pygame

from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece


class StarBase(GamePiece):
    """"""
    def __init__(self, screen: pygame.Surface):
        """"""
        super().__init__(screen, 'StarBase3.png')

    def update(self, sectorX, sectorY, playTime: float = 0):
        """"""
        super().update(sectorX, sectorY, playTime)
