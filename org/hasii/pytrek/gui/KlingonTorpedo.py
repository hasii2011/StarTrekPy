
from pygame import Surface


from org.hasii.pytrek.gui.BasicTorpedo import BasicTorpedo


class KlingonTorpedo(BasicTorpedo):

    def __init__(self, screen: Surface):
        """

        Args:
            screen:
        """
        super().__init__(screen, "images/KlingonTorpedo.png")
