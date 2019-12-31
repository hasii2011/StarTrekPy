
from logging import getLogger
from logging import Logger

import unittest

from tests.BaseTest import BaseTest

from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.ShieldHitData import ShieldHitData

from org.hasii.pytrek.objects.Coordinates import Coordinates

BASE_COORDINATES: Coordinates = Coordinates(4, 4)

#
# The following are all possible "docked" positions relative to the starbase
#
NORTH_COORDINATES: Coordinates = Coordinates(4, 3)
SOUTH_COORDINATES: Coordinates = Coordinates(4, 5)
EAST_COORDINATES:  Coordinates = Coordinates(3, 4)
WEST_COORDINATES:  Coordinates = Coordinates(5, 4)
NE_COORDINATES:    Coordinates = Coordinates(3, 3)
NW_COORDINATES:    Coordinates = Coordinates(5, 3)
SE_COORDINATES:    Coordinates = Coordinates(3, 5)
SW_COORDINATES:    Coordinates = Coordinates(5, 5)


class GameEngineTest(BaseTest):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger:      Logger     = getLogger(__name__)
        self.gameEngine:  GameEngine = GameEngine()

    def testRemainingGameTime(self):
        """"""
        self.logger.info("remainingGameTime %s", self.gameEngine.stats.remainingGameTime)
        self.assertIsNotNone(self.gameEngine.stats.remainingGameTime)

    def testRemainingKlingons(self):
        """"""
        self.logger.info("Initial Klingon count %s", self.gameEngine.stats.remainingKlingons)
        self.assertIsNotNone(self.gameEngine.stats.remainingKlingons)

    def testComputeEnergyForWarpTravel(self):
        """"""

    def testComputeHit(self):

        for pType in PlayerType:

            computedHit = self._commonComputeHit(playerType=pType)
            self.assertFalse(computedHit == 0.0, "Can't have non-hit")
            self.logger.info(f"computedHit for {pType.__repr__()}: {computedHit}")

    def testComputeShieldHit(self):

        for pType in PlayerType:
            torpedoHit:     float         = self._commonComputeHit(playerType=pType)
            shieldHitData:  ShieldHitData = self.gameEngine.computeShieldHit(torpedoHit=torpedoHit)
            self.logger.info(f"torpedoHit: f{torpedoHit:.2f}  {pType:19.19}  {shieldHitData}")

    def testIsShipAdjacentToBaseFalse(self):

        ans: bool = self.gameEngine.isShipAdjacentToBase(enterpriseLoc=Coordinates(0, 0), starbaseLoc=BASE_COORDINATES)
        self.assertFalse(ans, "False Test failed")

    def testIsShipAdjacentToBaseNorth(self):
        self._adjacentTest(NORTH_COORDINATES, "North code is broken")

    def testIsShipAdjacentToBaseSouth(self):
        self._adjacentTest(SOUTH_COORDINATES, "South code is broken")

    def testIsShipAdjacentToBaseEast(self):
        self._adjacentTest(EAST_COORDINATES, "East code is broken")

    def testIsShipAdjacentToBaseWest(self):
        self._adjacentTest(WEST_COORDINATES, "West code is broken")

    def testIsShipAdjacentToBaseNorthEast(self):
        self._adjacentTest(NE_COORDINATES, "Northeast code is broken")

    def testIsShipAdjacentToBaseNorthWest(self):
        self._adjacentTest(NW_COORDINATES, "Northwest code is broken")

    def testIsShipAdjacentToBaseSouthWest(self):
        self._adjacentTest(SW_COORDINATES, "Southwest code is broken")

    def testIsShipAdjacentToBaseSouthEast(self):
        self._adjacentTest(SE_COORDINATES, "Southeast code is broken")

    def _adjacentTest(self, testCoords: Coordinates, failMsg: str):

        ans: bool = self.gameEngine.isShipAdjacentToBase(enterpriseLoc=testCoords, starbaseLoc=BASE_COORDINATES)
        self.assertTrue(ans, failMsg)

    def _commonComputeHit(self, playerType: PlayerType) -> float:

        self.gameEngine.stats.skill = playerType

        shooterPosition: Coordinates = Coordinates(x=7, y=7)
        targetPosition:  Coordinates = Coordinates(x=3, y=7)
        klingonPower:    float       = 348.0

        computedHit = self.gameEngine.computeHit(shooterPosition=shooterPosition,
                                                 targetPosition=targetPosition,
                                                 klingonPower=klingonPower)

        return computedHit


if __name__ == '__main__':
    unittest.main()
