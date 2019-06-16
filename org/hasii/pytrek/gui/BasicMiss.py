
from pygame import Surface
import logging

from org.hasii.pytrek.gui.GamePiece import GamePiece


class BasicExplosion(GamePiece):

    DISPLAY_SECONDS = 5

    def __init__(self, screen: Surface, fileName: str, playTime: float):

        super().__init__(screen, fileName)

        self.logger = logging.getLogger(__name__)

        self.displayTime      = playTime
        self.eligibleToRemove = False

    def update(self, sectorX: int, sectorY: int, playTime: float = 0):
        """
        Display for DISPLAY_SECONDS;  Then tell controlling loop
        to remove

        :param sectorX:
        :param sectorY:
        :param playTime:
        :return:
        """

        timeSinceLastUpdate = playTime - self.displayTime
        if timeSinceLastUpdate < BasicExplosion.DISPLAY_SECONDS:
            super().update(sectorX, sectorY, playTime)
        else:
            self.eligibleToRemove = True


