
import pygame

from org.hasii.pytrek.engine import Direction
from org.hasii.pytrek.gui.gamepieces.BasicTorpedo import BasicTorpedo


class PhotonTorpedo(BasicTorpedo):
    """"""

    def __init__(self, screen: pygame.Surface, direction: Direction):
        """"""
        # filename = "images/torpedo_{}.png".format(direction.name)
        filename: str = f'torpedo_{direction.name}.png'
        super().__init__(screen, filename)
