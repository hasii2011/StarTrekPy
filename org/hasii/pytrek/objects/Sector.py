
from pygame.sprite import Sprite

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.SectorType import SectorType


class Sector:
    """"""
    def __init__(self, sprite: Sprite, sectorType: SectorType, sectorX: int, sectorY: int):
        """
        Initialize the sector's settings if the sector is empty the sprite will be null

        Args:
            sprite:     The sprite in this sector;  May be None
            sectorType: What type of sector see SectorType
            sectorX:    The sector's X position
            sectorY:    The sector's Y position
        """
        self.sprite     = sprite
        self.sectorType = sectorType
        self.sectorX    = sectorX
        self.sectorY    = sectorY

    def setCoordinates(self, coordinates: Coordinates):
        """"""
        self.sectorX = coordinates.getX()
        self.sectorY = coordinates.getY()

    def getCoordinates(self) -> Coordinates:
        """"""
        coordinate = Coordinates(x=self.sectorX, y=self.sectorY)
        return coordinate

    def setType(self, sectorType: SectorType):
        """

        Args:
            sectorType:  the type of sector to make this

        """
        self.sectorType = sectorType

    def getType(self) -> SectorType:
        """
        Returns: The sector type
        """
        return self.sectorType

    def setSprite(self, theSprite: Sprite):
        """"""
        self.sprite = theSprite

    def __str__(self) -> str:
        """"""
        return f"SectorType: {str(self.sectorType)}  Coordinates ({str(self.sectorX)},{str(self.sectorY)})"
