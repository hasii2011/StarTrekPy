import pygame

from org.hasii.pytrek.gui.gamepieces.BasicMiss import BasicMiss


class KlingonTorpedoMiss(BasicMiss):

    DISPLAY_SECONDS: int = 5
    FILENAME:        str = "KlingonTorpedoMiss.png"

    def __init__(self, screen: pygame.Surface, playTime: float):
        """"""

        super().__init__(screen=screen, fileName=KlingonTorpedoMiss.FILENAME, playTime=playTime)
