import unittest
import logging
import jsonpickle

from BaseTest import BaseTest

from org.hasii.pytrek.GameStatistics import GameStatistics
from org.hasii.pytrek.engine.GameType import GameType
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.objects import Coordinates
from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.engine.ComputerStatus import ComputerStatus


class GameStatisticsTest(BaseTest):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger = logging.getLogger(__name__)

    def testSingletonBehavior(self):

        gsst         = GameStatistics()
        doppleGanger = GameStatistics()

        self.assertEqual(gsst, doppleGanger, "Singleton creation failed")

        self.logger.info("gsst: '%s',  doppleGanger: '%s'", gsst.__repr__(), doppleGanger.__repr__())

    def testJsonSerialization(self):

        gsst          = GameStatistics()
        gsst.skill    = PlayerType.Emeritus
        gsst.gameType = GameType.Medium
        gsst.starDate = 40501.0
        gsst.computerStatus = ComputerStatus.Down
        gsst.currentQuadrantCoordinates = Coordinates(4, 4)
        gsst.currentSectorCoordinates   = Coordinates(9, 9)

        jsonGsst = jsonpickle.encode(gsst)
        self.assertIsNotNone(jsonGsst, "Pickling failed")

        self.logger.info("json game stats: '%s", jsonGsst)

        file = open('GameStats.json', 'w')
        file.write(jsonGsst)
        file.close()

        jsonFile = open("GameStats.json", 'r')
        jsonStr  = jsonFile.read()
        self.assertIsNotNone(jsonStr)
        jsonFile.close()

        thawedGameGsst = jsonpickle.decode(jsonStr)
        self.assertIsNotNone(thawedGameGsst, "Did that thaw")

        self.assertEqual(gsst.skill,          thawedGameGsst.skill,          "Skill did not thaw")
        self.assertEqual(gsst.starDate,       thawedGameGsst.starDate,       "Star date did not thaw")
        self.assertEqual(gsst.computerStatus, thawedGameGsst.computerStatus, "Computer status did not thaw")


if __name__ == '__main__':
    unittest.main()