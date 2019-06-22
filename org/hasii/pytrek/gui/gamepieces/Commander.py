import logging
import random

from pygame import Surface

from org.hasii.pytrek.engine.Direction import Direction
from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.objects.Coordinates import Coordinates


class Commander(GamePiece):
    """"""

    UPDATE_INTERVAL_SECONDS = 7

    def __init__(self, screen: Surface, coordinates: Coordinates):
        """"""
        super().__init__(screen, 'images/medfighter.png')

        self.logger = logging.getLogger(__name__)

        self.currentPosition   = coordinates
        self.timeSinceMovement = 0
        self._power = 0.0

    def getPower(self) -> float:
        return self._power

    def setPower(self, theNewValue: float):
        self._power = theNewValue

    def update(self, sectorX, sectorY, playTime: float = 0) -> Coordinates:
        """"""

        self.currentPosition.x = sectorX
        self.currentPosition.y = sectorY
        timeSinceLastUpdate = playTime - self.timeSinceMovement

        if timeSinceLastUpdate > Commander.UPDATE_INTERVAL_SECONDS:
            self.logger.debug(f"'{Commander.UPDATE_INTERVAL_SECONDS}' seconds have elapsed;  Commander will move")
            self.currentPosition   = self.evade(self.currentPosition)
            self.timeSinceMovement = playTime

        super().update(self.currentPosition.x, self.currentPosition.y)

        return self.currentPosition

    def evade(self, currentLocation: Coordinates) -> Coordinates:
        """
        Move commander around to avoid torpedoes

        :return: new random coordinates
        """
        while True:
            pDirection:     Direction   = self._randomDirection_()
            newCoordinates: Coordinates = currentLocation.newCoordinates(pDirection)

            self.logger.debug("Random direction %s: currentLocation: %s newCoordinates %s", pDirection.name, currentLocation, newCoordinates)
            if newCoordinates.valid():
                break
        return newCoordinates

    def _randomDirection_(self) -> Direction:
        """"""
        return random.choice(list(Direction))
