import pygame

from hasii.pytrek.gui.gamepieces.BasicMiss import BasicMiss


class BigRedX(BasicMiss):

    DISPLAY_SECONDS: int = 5
    FILENAME:        str = "images/BigRedX_32x32.png"

    def __init__(self, screen: pygame.Surface, playTime: float):
        """"""

        super().__init__(screen=screen, fileName=BigRedX.FILENAME, playTime=playTime)

    #     self.logger           = logging.getLogger(__name__)
    #     self.displayTime      = playTime
    #     self.eligibleToRemove = False
    #
    # def update(self, sectorX: int, sectorY: int, playTime: float = 0):
    #     """
    #     Display for DISPLAY_SECONDS;  Then tell controlling loop
    #     to remove
    #
    #     :param sectorX:
    #     :param sectorY:
    #     :param playTime:
    #     :return:
    #     """
    #
    #     timeSinceLastUpdate = playTime - self.displayTime
    #     if timeSinceLastUpdate < BigRedX.DISPLAY_SECONDS:
    #         super().update(sectorX, sectorY, playTime)
    #     else:
    #         self.eligibleToRemove = True
