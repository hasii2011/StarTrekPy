
import logging

from pygame import Surface

from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece


class BasicMiss(GamePiece):

    DISPLAY_SECONDS = 5

    def __init__(self, screen: Surface, fileName: str, playTime: float):

        super().__init__(screen, fileName)

        self.logger           = logging.getLogger(__name__)
        self.displayTime      = playTime
        self.eligibleToRemove = False

    def update(self, sectorX: int, sectorY: int, playTime: float = 0):
        """

        Display for DISPLAY_SECONDS;  Then mark as eligible to remove

        Args:
            sectorX:
            sectorY:
            playTime:

        Returns:

        """

        timeSinceLastUpdate = playTime - self.displayTime
        if timeSinceLastUpdate < BasicMiss.DISPLAY_SECONDS:
            super().update(sectorX, sectorY, playTime)
        else:
            self.eligibleToRemove = True
