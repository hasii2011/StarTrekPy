
from pygame import Surface


from hasii.pytrek.gui.gamepieces.BasicTorpedo import BasicTorpedo

from org.hasii.pytrek.objects.Coordinates import Coordinates


class KlingonTorpedo(BasicTorpedo):

    def __init__(self, screen: Surface, shooterPower: float, shooterPosition: Coordinates):
        """

        Args:
            screen:
        """
        super().__init__(screen, "images/KlingonTorpedo.png")
        self.shooterPower:    float       = shooterPower
        self.shooterPosition: Coordinates = shooterPosition
