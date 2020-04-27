import pygame

from org.hasii.pytrek.gui.gamepieces.BasicMiss import BasicMiss


class BigRedX(BasicMiss):

    DISPLAY_SECONDS: int = 5
    FILENAME:        str = "BigRedX_32x32.png"

    def __init__(self, screen: pygame.Surface, playTime: float):
        """"""

        super().__init__(screen=screen, fileName=BigRedX.FILENAME, playTime=playTime)
