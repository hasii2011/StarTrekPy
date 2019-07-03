
from typing import cast
from typing import List

import logging

from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Quadrant import Quadrant

from org.hasii.pytrek.GameStatistics import GameStatistics


class Galaxy:
    """Galaxy management"""

    def __init__(self, screen, intelligence, gameEngine):
        """"""
        self.screen         = screen
        self.intelligence   = intelligence
        self.gameEngine     = gameEngine

        self.stats          = GameStatistics()
        self.settings       = Settings()
        self.logger         = logging.getLogger(__name__)

        self.starBaseCount: int = 0
        self.planetCount:   int = 0
        self.gameParameters:  GameStatistics = cast(typ=GameStatistics, val=None)
        self.currentQuadrant: Quadrant       = cast(typ=Quadrant, val=None)
        self.quadrants = []  # 2D array aka python list

        self.createGalaxy(screen)

        self.placeKlingonsInGalaxy()
        self.placeCommandersInGalaxy()
        self.placeStarBasesInGalaxy()
        self.setInitialQuadrant()

    def createGalaxy(self, screen):

        self.quadrants = []
        for x in range(Intelligence.GALAXY_WIDTH):
            col = []
            for y in range(Intelligence.GALAXY_HEIGHT):
                coordinates = Coordinates(x, y)
                quadrant = Quadrant(coordinates, screen)
                col.append(quadrant)
                self.logger.debug("Created quadrant: (%s,%s)", str(x), str(y))
            self.quadrants.append(col)

    def updateGalaxy(self):
        """"""

    def setInitialQuadrant(self):
        """"""
        coordinates = self.intelligence.getRandomQuadrantCoordinates()
        self.logger.info("Current Quadrant set to: %s", coordinates)
        row = self.quadrants[coordinates.getX()]
        self.currentQuadrant = row[coordinates.getY()]

    def getCurrentQuadrant(self) -> Quadrant:
        """"""
        return self.currentQuadrant

    def placeKlingonsInGalaxy(self):
        """"""
        for x in range(self.stats.remainingKlingons):
            coordinates = self.intelligence.getRandomQuadrantCoordinates()
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addKlingon()
        self.debugPrintKlingonPlacement()

    def placeCommandersInGalaxy(self):
        """"""
        for x in range(self.stats.remainingCommanders):
            coordinates = self.intelligence.getRandomQuadrantCoordinates()
            quadrant    = self.getQuadrant(coordinates)
            quadrant.addCommander()

    def placeStarBasesInGalaxy(self):
        """"""
        starBaseCount = self.intelligence.getInitialStarBaseCount()
        while starBaseCount != 0:
            quadrantCoordinates = self.intelligence.getRandomQuadrantCoordinates()
            quadrant            = self.getQuadrant(quadrantCoordinates)
            while quadrant.hasStarBase() is True:
                quadrantCoordinates = self.intelligence.getRandomQuadrantCoordinates()
                quadrant = self.getQuadrant(quadrantCoordinates)

            self.logger.debug(f"Starbase at quadrant {quadrantCoordinates}")
            quadrant.addStarBase()
            starBaseCount -= 1

    def getQuadrant(self, quadrantCoordinates: Coordinates) -> Quadrant:

        quadrantRow = self.quadrants.__getitem__(quadrantCoordinates.getX())
        quadrant    = quadrantRow.__getitem__(quadrantCoordinates.getY())

        return quadrant

    def debugPrintKlingonPlacement(self):
        """"""
        for x in range(Intelligence.GALAXY_HEIGHT):
            quadRow = self.quadrants[x]
            for y in range(Intelligence.GALAXY_WIDTH):
                quadrant = quadRow[y]
                self.logger.debug("Quadrant(%s,%s) Klingon Count %s", x, y, str(quadrant.getKlingonCount()))
