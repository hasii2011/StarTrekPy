import pygame
import logging

from org.hasii.pytrek.gui.GamePiece import GamePiece


class BigRedX(GamePiece):

    DISPLAY_SECONDS = 5

    def __init__(self, screen: pygame.Surface, playTime: float):
        """"""

        filename = "images/BigRedX_32x32.png"
        super().__init__(screen, filename)

        self.logger           = logging.getLogger(__name__)
        self.displayTime      = playTime
        self.eligibleToRemove = False

    def update(self, sectorX: int, sectorY: int, playTime: float):
        """
        Display for DISPLAY_SECONDS;  Then tell controlling loop
        to remove

        :param sectorX:
        :param sectorY:
        :param playTime:
        :return:
        """

        timeSinceLastUpdate = playTime - self.displayTime
        if timeSinceLastUpdate < BigRedX.DISPLAY_SECONDS:
            super().update(sectorX, sectorY,playTime)
        else:
            self.eligibleToRemove = True
