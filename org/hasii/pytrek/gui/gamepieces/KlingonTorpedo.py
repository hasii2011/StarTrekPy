
from pygame import Surface


from org.hasii.pytrek.gui.gamepieces.BasicTorpedo import BasicTorpedo

from org.hasii.pytrek.objects.Coordinates import Coordinates


class KlingonTorpedo(BasicTorpedo):

    def __init__(self, screen: Surface, shooterPower: float, shooterPosition: Coordinates):
        """

        Args:
            screen:             pygame place to draw
            shooterPower:       The shooter's power
            shooterPosition:    The shooter's position
        """

        super().__init__(screen, "images/KlingonTorpedo.png")
        self.shooterPower:    float       = shooterPower
        self.shooterPosition: Coordinates = shooterPosition
