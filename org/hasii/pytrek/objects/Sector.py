
from org.hasii.pytrek.objects.Coordinates import Coordinates

class Sector:
    """"""
    def __init__(self, sprite, sectorType, sectorX, sectorY):
        """
        Initialize the sector's settings if the sector is empty the sprite will be null

        :param sprite:  The sprite in this sector;  May be null

        :param sectorType:  What type of sector see SectorType

        :param sectorX: The sector's X position

        :param sectorY: The sector's Y position
        """

        self.sprite     = sprite
        self.sectorType = sectorType
        self.sectorX    = sectorX
        self.sectorY    = sectorY

    def setCoordinates(self, coordinate):
        """"""
        self.sectorX = coordinate.getX()
        self.sectorY = coordinate.getY()

    def getCoordinates(self)->Coordinates:
        """"""

        coordinate = Coordinates(x=self.sectorX, y=self.sectorY)
        return coordinate

    def setType(self, sectorType):
        """

        :param sectorType: the type of sector to make this

        :return: None
        """
        self.sectorType = sectorType
    def getType(self):
        """

        :return: the sector type
        """
        return self.sectorType
    def setSprite(self, theSprite):
        """"""
        self.sprite = theSprite

    def __str__(self) -> str:
        """"""
        return "SectorType: " + str(self.sectorType) + " Coordinates (" + str(self.sectorX) + "," + str(self.sectorY) + ")"

