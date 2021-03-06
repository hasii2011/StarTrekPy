
from typing import List

import logging
import unittest

from tests.BaseTest import BaseTest

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.gui.gamepieces.Klingon import Klingon

from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.GameType import GameType

from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.DeviceType import DeviceType
from org.hasii.pytrek.engine.MoveBaddyData import MoveBaddyData

from org.hasii.pytrek.objects.Galaxy import Galaxy
from org.hasii.pytrek.objects.Quadrant import Quadrant
from org.hasii.pytrek.objects.Coordinates import Coordinates


class IntelligenceTest(BaseTest):
    """
    hee hee
    """

    DEFAULT_GAME_LENGTH         = 210.00
    EXPECTED_SHORT_GAME_LENGTH  = 56
    EXPECTED_LONG_GAME_LENGTH   = 224
    EXPECTED_MEDIUM_GAME_LENGTH = 112
    MAX_RANDOM_TIME_CALLS       = 10
    MAX_STAR_DATE_CALLS         = 7
    #
    # Need to know this cuz' commander count depends on this value
    #
    KNOWN_KLINGON_COUNT = 48

    DEFAULT_AVERAGE = 7.0
    BIG_HIT_VALUE   = 900.42
    SMALL_HIT_VALUE = 25.25

    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.settings = Settings()
        self.smarty   = Intelligence()
        self.devices  = Devices()
        self.gameEngine = GameEngine()

        self.galaxy   = Galaxy(screen=None, intelligence=self.smarty, gameEngine=self.gameEngine)

        self.logger   = logging.getLogger(__name__)

    def testGetRandomSectorCoordinates(self):
        """"""
        coordinates = self.smarty.getRandomSectorCoordinates()
        self.assertIsNotNone(coordinates, "Should not be null")
        self.logger.info("random coordinates: '%s'", coordinates)

        bogusCoordinate = Coordinates(-1, -1)

        self.assertNotEqual(coordinates, bogusCoordinate, "Not truly initializing random coordinates")

    def testGetInitialStarBaseCount(self):
        """"""
        minStarBases  = self.settings.starBaseMinimum
        maxStarBases  = self.settings.starBaseMaximum
        starBaseCount = self.smarty.getInitialStarBaseCount()

        self.logger.info("starBaseCount: %s", starBaseCount)
        self.assertGreaterEqual(starBaseCount, minStarBases, "Failed too few star bases")
        self.assertLessEqual(starBaseCount,    maxStarBases, "Failed too many star bases")

    def testInitialKlingonCountPlayerTypeNoviceGameTypeShort(self):
        """"""

        settings            = Settings()
        settings.skill      = PlayerType.Novice
        settings.gameType   = GameType.Short

        intelligence = Intelligence()

        klingonCount = intelligence.getInitialKlingonCount(remainingGameTime=IntelligenceTest.DEFAULT_GAME_LENGTH)

        self.assertIsNotNone(klingonCount, "I need some value back")

    def testInitialKlingonCountPlayerTypeEmeritusGameTypeLong(self):
        """"""

        settings          = Settings()
        settings.skill    = PlayerType.Emeritus
        settings.gameType = GameType.Long

        intelligence = Intelligence()
        klingonCount = intelligence.getInitialKlingonCount(remainingGameTime=IntelligenceTest.DEFAULT_GAME_LENGTH)
        self.assertIsNotNone(klingonCount, "I need some klingon value back")

    def testGetGameInitialTimeShort(self):
        """"""
        self.settings.gameType = GameType.Short

        gameTime = self.smarty.getInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(IntelligenceTest.EXPECTED_SHORT_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeLong(self):
        """"""
        self.settings.gameType = GameType.Long

        gameTime = self.smarty.getInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(IntelligenceTest.EXPECTED_LONG_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialGameTimeMedium(self):
        """"""
        self.settings.gameType = GameType.Medium

        gameTime = self.smarty.getInitialGameTime()

        self.assertIsNotNone(gameTime, "I need some time value back")
        self.assertEqual(IntelligenceTest.EXPECTED_MEDIUM_GAME_LENGTH, gameTime, "Looks like game length factor changed")

    def testGetInitialCommandersCountPlayerTypeNovice(self):
        """"""
        self._setupCommandersTest(PlayerType.Novice)
        commanderCount = self.smarty.getInitialCommanderCount()

        self.assertIsNotNone(commanderCount)
        self.logger.info("commander count '%s', skill: '%s'", commanderCount, PlayerType.Novice.name)

        adjustedKlingonCount = IntelligenceTest.KNOWN_KLINGON_COUNT - commanderCount
        self.assertEqual(adjustedKlingonCount, self.smarty.remainingKlingons, "Klingon count should be adjusted by commander count")

    def testGetInitialCommandersCountPlayerTypeFair(self):
        """"""
        self._setupCommandersTest(PlayerType.Fair)
        commanderCount = self.smarty.getInitialCommanderCount()

        self.assertIsNotNone(commanderCount)
        self.logger.info("commander count '%s', skill: '%s'", commanderCount, PlayerType.Fair.name)

        adjustedKlingonCount = IntelligenceTest.KNOWN_KLINGON_COUNT - commanderCount
        self.assertEqual(adjustedKlingonCount, self.smarty.remainingKlingons, "Klingon count should be adjusted by commander count")

    def testGetInitialCommandersCountPlayerTypeGood(self):
        """"""
        self._setupCommandersTest(PlayerType.Good)
        commanderCount = self.smarty.getInitialCommanderCount()

        self.assertIsNotNone(commanderCount)
        self.logger.info("commander count '%s', skill: '%s'", commanderCount, PlayerType.Good.name)

        adjustedKlingonCount = IntelligenceTest.KNOWN_KLINGON_COUNT - commanderCount
        self.assertEqual(adjustedKlingonCount, self.smarty.remainingKlingons, "Klingon count should be adjusted by commander count")

    def testGetInitialCommandersCountPlayerTypeExpert(self):
        """"""
        self._setupCommandersTest(PlayerType.Expert)
        commanderCount = self.smarty.getInitialCommanderCount()

        self.assertIsNotNone(commanderCount)
        self.logger.info("commander count '%s', skill: '%s'", commanderCount, PlayerType.Expert.name)

        adjustedKlingonCount = IntelligenceTest.KNOWN_KLINGON_COUNT - commanderCount
        self.assertEqual(adjustedKlingonCount, self.smarty.remainingKlingons, "Klingon count should be adjusted by commander count")

    def testGetInitialCommandersCountPlayerTypeEmeritus(self):
        """"""
        self._setupCommandersTest(PlayerType.Emeritus)
        commanderCount = self.smarty.getInitialCommanderCount()

        self.assertIsNotNone(commanderCount)
        self.logger.info("commander count '%s', skill: '%s'", commanderCount, PlayerType.Emeritus.name)

        adjustedKlingonCount = IntelligenceTest.KNOWN_KLINGON_COUNT - commanderCount
        self.assertEqual(adjustedKlingonCount, self.smarty.remainingKlingons, "Klingon count should be adjusted by commander count")

    def testComputeRandomTimeInterval(self):
        """"""

        for x in range(0, IntelligenceTest.MAX_RANDOM_TIME_CALLS):
            randomTime: float = self.smarty.computeRandomTimeInterval()
            self.logger.debug("randomTime '%s", randomTime)
            self.assertGreaterEqual(randomTime, Intelligence.RANDOM_TIME_INTERVAL_START, "Random less than possible")
            self.assertLessEqual(randomTime, Intelligence.RANDOM_TIME_INTERVAL_END, "Random time greater than possible")

    def testGetInitialStarDate(self):

        for x in range(0, IntelligenceTest.MAX_STAR_DATE_CALLS):
            starDate: int = self.smarty.getInitialStarDate()
            self.assertIsNotNone(starDate)
            self.assertGreater(starDate, 0, "No such thing as a 0 star date")
            self.logger.info("Initial stardate '%s'", starDate)

    def testRand(self):

        for x in range(0, 1000):
            ans = self.smarty.rand()
            self.logger.info(f"Iteration {x}, answer is {ans}")

    def testComputeKlingonPower(self):

        self.logger.info("")
        for skill in PlayerType:

            self.smarty.skill = skill

            klingonPower: float = self.smarty.computeKlingonPower()
            self.logger.info(f"Klingon power: {klingonPower},  Skill: {self.smarty.skill}")
            self.assertGreater(klingonPower, 0, "Should get some value")

    def testComputeCommanderPower(self):

        self.logger.info("")
        for skill in PlayerType:

            self.smarty.skill = skill

            commanderPower: float = self.smarty.computeCommanderPower()
            self.logger.info(f"Commander power: {commanderPower},  Skill: {self.smarty.skill}")
            self.assertGreater(commanderPower, 0, "Should get some value")

    def testExpRan(self):

        self.logger.info(f"DEFAULT: {IntelligenceTest.DEFAULT_AVERAGE}")
        ans: float = self.smarty.expRan(IntelligenceTest.DEFAULT_AVERAGE)

        self.logger.info(f"avrage: {IntelligenceTest.DEFAULT_AVERAGE} ans: {ans:4f}")

        ans2: float = self.smarty.expRan(56.0)
        self.logger.info(f"avrage: '56.0'  ans2: {ans2:4f}")

        self.settings.gameType = GameType.Long
        initGameTime: float = self.smarty.getInitialGameTime()
        ans3: float = self.smarty.expRan(initGameTime)
        self.logger.info(f"avrage: '{initGameTime}'  ans2: {ans3:4f}")

    def testEnumerateStringDeviceTypes(self):

        self.logger.info("Device Types")
        for deviceType in DeviceType:
            self.logger.info(f"{deviceType}")

        self.logger.info("Player Type Values")
        for playerType in PlayerType:
            self.logger.info(f"PlayerType: '{playerType}' -- value '{playerType.value}'")

    def testIsCriticalHit(self):

        hitsToCheck = [100, 200, 300]
        self.logger.info(f"Hits to check: {hitsToCheck}")
        self.smarty.skill = PlayerType.Emeritus
        for val in hitsToCheck:
            ans: bool = self.smarty.isCriticalHit(val)
            self.logger.info(f"answer: {ans}")

    def testGetRandomDevice(self):

        for x in range(1000):
            randomDevice: DeviceType = self.smarty._getRandomDevice()
            self.logger.info(f"randomDevice: {randomDevice}")
            self.assertIsNotNone(randomDevice)

    def testFryDevices(self):

        self.logger.info(f"Device List before Fry: {self.devices}")

        damagedDeviceType: DeviceType = self.smarty.fryDevice(IntelligenceTest.BIG_HIT_VALUE)
        self.assertIsNotNone(damagedDeviceType, "Oops should have been a critical hit.")
        self.logger.info(f"damagedDeviceType {damagedDeviceType}")

        damagedDeviceType = self.smarty.fryDevice(IntelligenceTest.SMALL_HIT_VALUE)
        self.assertIsNone(damagedDeviceType, "Should not have been a critical hit")
        self.logger.info(f"damagedDeviceType {damagedDeviceType}")

    def testMoveBaddy(self):

        currentQuadrant: Quadrant = self.galaxy.currentQuadrant
        while currentQuadrant.getKlingonCount() <= 0:
            self.logger.info(f"No klingons in quadrant: {currentQuadrant.coordinates}")
            #
            # generate a new random quadrant
            self.galaxy.setInitialQuadrant()
            currentQuadrant = self.galaxy.currentQuadrant

        klingons: List[Klingon] = currentQuadrant.getKlingons()

        baddyData: MoveBaddyData = MoveBaddyData(playerSkill=PlayerType.Emeritus, numberOfKlingons=2, numberOfCommanders=1)

        self.smarty.moveBaddy(moveBaddyData=baddyData, baddyLocation=klingons[0].currentPosition)
        self.logger.info(f"Did the baddy move?")

    def _setupCommandersTest(self, skill: PlayerType):
        """"""
        # settings        = Settings()
        self.settings.skill  = skill
        self.smarty.remainingKlingons = IntelligenceTest.KNOWN_KLINGON_COUNT


if __name__ == '__main__':
    unittest.main()
