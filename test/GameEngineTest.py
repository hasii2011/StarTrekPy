import logging
import logging.config

import unittest

from BaseTest import BaseTest
from org.hasii.pytrek.engine.GameEngine import GameEngine

class GameEngineTest(BaseTest):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger     = logging.getLogger(__name__)
        self.gameEngine = GameEngine()

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

if __name__ == '__main__':
    unittest.main()