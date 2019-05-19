
from pygame import Surface

from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.objects.Coordinates import Coordinates


class Klingon(GamePiece):
    """"""

    power: float = 0

    def __init__(self, screen: Surface, coordinates: Coordinates):
        """"""
        super().__init__(screen, 'images/KlingonD7.png')
        self.currentPosition = coordinates

    def update(self, sectorX, sectorY):
        """"""
        super().update(sectorX, sectorY)