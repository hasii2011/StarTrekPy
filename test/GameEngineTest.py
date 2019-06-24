import logging
import logging.config

import unittest

from test.BaseTest import BaseTest

from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.ShieldHitData import ShieldHitData

from org.hasii.pytrek.objects.Coordinates import Coordinates


class GameEngineTest(BaseTest):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger       = logging.getLogger(__name__)
        self.gameEngine   = GameEngine()

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
