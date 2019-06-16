
from pygame import Surface

from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.objects.Coordinates import Coordinates


class Klingon(GamePiece):
    """"""

    def __init__(self, screen: Surface, coordinates: Coordinates):
        """"""
        super().__init__(screen, 'images/KlingonD7.png')
        self.currentPosition = coordinates
        self._power = 0.0

    def getPower(self) -> float:
        return self._power

    def setPower(self, theNewValue: float):
        self._power = theNewValue

    def update(self, sectorX, sectorY, playTime: float = 0):
        """"""
        super().update(sectorX, sectorY)
