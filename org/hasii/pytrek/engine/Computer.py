
import math
import logging
import random

from typing import List
from typing import cast

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Quadrant import Quadrant

from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.engine.Direction import Direction
from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece


class Computer:
    """
    Make a computer a singleton so we don't have to pass it around
    """
    QUADRANT_TRAVEL_FACTOR = 0.1
    GALACTIC_TRAVEL_FACTOR = 1.0

    _singleton  = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(Computer)
            cls._singleton.__initialized = False

        return cls._singleton

    def __init__(self):
        """"""

        if self.__initialized is True:
            return
        else:
            self.__initialized = True

        self.settings = Settings()
        self.logger   = logging.getLogger(__name__)

    def computeQuadrantDistance(self, startSector: Coordinates, endSector: Coordinates) -> float:
        """"""
        return self.computeDistance(startSector, endSector, Computer.QUADRANT_TRAVEL_FACTOR)

    def computeGalacticDistance(self, startQuadrantCoordinates: Coordinates, endQuadrantCoordinates: Coordinates) -> float:
        """"""
        return self.computeDistance(startQuadrantCoordinates, endQuadrantCoordinates, Computer.GALACTIC_TRAVEL_FACTOR)

    def computeSectorCoordinates(self, xPos: int, yPos: int) -> Coordinates:
        """From a pygame screen position determine which sector in quadrant"""

        return self.computeCoordinates(xPos=xPos, yPos=yPos)

    def computeQuadrantCoordinates(self, xPos: int, yPos: int) -> Coordinates:
        """"""
        return self.computeCoordinates(xPos=xPos, yPos=yPos)

    def computeCoordinates(self, xPos: int, yPos: int) -> Coordinates:
        """"""
        gameX =  int(math.floor(xPos / GamePiece.QUADRANT_PIXEL_WIDTH))
        gameY =  int(math.floor(yPos / GamePiece.QUADRANT_PIXEL_HEIGHT))

        coordinates = Coordinates(gameX, gameY)

        return coordinates

    def createValueString(self, quadrant: Quadrant) -> str:
        """This is a duplicate of the code in the GalaxyScanBackground sprite
        I needed to test it but sprites need pygame Surface's
        Did not know how to create one for a unit test

        """

        klingonCount = quadrant.getKlingonCount()
        klingonCount = klingonCount + quadrant.commanderCount
        quadrantValue = klingonCount * 100
        if quadrant.hasStarBase():
            quadrantValue += 10

        strValue = str(quadrantValue).rjust(3, '0')

        return strValue

    def computeDistance(self, startCoordinates: Coordinates, endCoordinates: Coordinates, travelFactor: float) -> float:
        """

         x1 = startSector.getX()
         y1 = startSector.getY()
         x2 = endSector.getX()
         y2 = endSector.getY()

         deltaX = x2 - x1
         deltaY = y2 - y1

         distance = travelFactor * math.sqrt( (deltaX * deltaX) + (deltaY * deltaY) )

        :param startCoordinates:
        :param endCoordinates:
        :param travelFactor accounts for quadrant travel or galactic travel

        :return: The game distance between the above
        """

        x1 = startCoordinates.getX()
        y1 = startCoordinates.getY()
        x2 = endCoordinates.getX()
        y2 = endCoordinates.getY()

        self.logger.debug("x1: %s y1: %s x2: %s  y2: %s", x1, y1, x2, y2)

        deltaX = x2 - x1
        deltaY = y2 - y1
        self.logger.debug("deltaX: %s deltaY: %s", deltaX, deltaY)
        self.logger.debug("deltaX: %s deltaY: %s", deltaX, deltaY)

        distance = travelFactor * math.sqrt((deltaX * deltaX) + (deltaY * deltaY))

        self.logger.debug("Quadrant Distance: %s", distance)
        return distance

    def interpolateYIntercepts(self, start: Coordinates, end: Coordinates) -> List:
        """
        Interpolate the coordinates between the start and end coordinates.  The grid
        we implemented is oriented in Quadrant IV;

           y = y0 + α(y1 - y0)

        :param start:
        :param end:
        :return:
        """

        x0 = start.getX()
        y0 = start.getY()
        x1 = end.getX()
        y1 = end.getY()

        if x0 == x1:
            return self.doStraightLineInterpolation(x0, y0, y1)

        interceptCoordinates = []
        if x0 < x1:
            i: int = x0 + 1
            while i < end.getX():
                coordinate: Coordinates = self.calcCoordinate(i, x0, x1, y0, y1)
                interceptCoordinates.append(coordinate)
                i = i + 1
        else:
            i: int = x0 - 1
            while i >= x1:
                coordinate: Coordinates = self.calcCoordinate(i, x0, x1, y0, y1)
                interceptCoordinates.append(coordinate)
                i = i - 1

        # if len(interceptCoordinates) == 0:
        interceptCoordinates.append(end)

        return interceptCoordinates

    def doStraightLineInterpolation(self, x0: int, y0: int, y1: int):
        """"""

        interceptCoordinates = []

        if y0 < y1:
            y = y0 + 1
            while True:
                c = Coordinates(x0, y)
                interceptCoordinates.append(c)
                y = y + 1
                if y >= y1:
                    break
        else:
            y = y0 - 1
            while True:
                c = Coordinates(x0, y)
                interceptCoordinates.append(c)
                y = y - 1
                if y <= y1:
                    break

        c = Coordinates(x0, y1)
        interceptCoordinates.append(c)
        return interceptCoordinates

    def calcCoordinate(self, i, x0, x1, y0, y1) -> Coordinates:
        """"""

        x     = i
        alpha = self.calculateAlpha(x0, x1, x)
        y     = y0 + alpha * (y1 - y0)

        coordinate: Coordinates = Coordinates(i, round(y))
        return coordinate

    def calculateAlpha(self, x0: int, x1: int, x: int) -> float:
        """"""

        alpha = (x - x0) / (x1 - x0)

        return alpha

    def determineDirection(self, startCoordinates: Coordinates, endCoordinates: Coordinates) -> Direction:
        """"""

        startX: int = startCoordinates.getX()
        startY: int = startCoordinates.getY()
        endX:   int = endCoordinates.getX()
        endY:   int = endCoordinates.getY()

        answer: Direction = cast(Direction, None)

        if startX == endX:
            if startY < endY:
                answer = Direction.South
            elif startY > endY:
                answer = Direction.North
        elif startY == endY:
            if startX < endX:
                answer = Direction.East
            elif startX > endX:
                answer = Direction.West
        elif startX < endX and startY < endY:
            answer = Direction.SouthEast
        elif startX > endX and startY > endY:
            answer = Direction.NorthWest
        elif startX < endX and startY > endY:
            answer = Direction.NorthEast
        elif startX > endX and startY < endY:
            answer = Direction.SouthWest

        return answer

    def randomDirection(self) -> Direction:
        """"""
        return random.choice(list(Direction))

    def computeHitValueOnEnterprise(self, klingonPosition: Coordinates, enterprisePosition: Coordinates, klingonPower: float) -> float:
        """
        :return:
        """

        distance:  float = self.computeQuadrantDistance(startSector=klingonPosition, endSector=enterprisePosition)
        hitFactor: float = 1.3 - distance
        hit:       float = klingonPower * hitFactor
        return hit

    def _computeCourse(self, start: Coordinates, end: Coordinates) -> float:
        """

        /* Enemy used photon torpedo */
        double course = 1.90985 * atan2((double)secty-jy, (double)jx-sectx);

        :param start:
        :param end:
        :return:
        """
        jx    = start.getX()
        jy    = start.getY()
        sectx = end.getX()
        secty = end.getY()

        course: float = 1.90985 * math.atan2((secty - jy), (jx - sectx))

        return course

    def _randomizeAttackerPower(self, attackerPower: float) -> float:
        """

        r = (Rand()+Rand())*0.5 -0.5;
        r += 0.002*kpower[l]*r;

        Rand() is SST's version
         double in the range 0.0 to 1.0
        :param attackerPower:
        :return:
        """

        r = (random.random() + random.random()) * 0.5 - 0.5
        r += 0.002 * attackerPower * r
        r = math.fabs(r)
        return r

    def _square(self, num: float):
        """
        Emulates sst square()

            double square(double i) { return i*i; }

        :param num:
        :return:
        """
        return num * num

    def __repr__(self):
        return '<%s at %s>' % (self.__class__.__name__, hex(id(self)))
