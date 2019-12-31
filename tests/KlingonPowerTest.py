
import logging

from tests.BaseTest import BaseTest

from org.hasii.pytrek.engine.KlingonPower import KlingonPower


class KlingonPowerTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""

        self.logger = logging.getLogger(__name__)

    def testNoviceKlingonPower(self):

        playerTypeStr: str = KlingonPower.Novice.name
        self.logger.info("playerTypeStr: %s", playerTypeStr)

        self.doTest(playerTypeStr, KlingonPower.Novice.value, "Novice value failed")

    def testFairKlingonPower(self):
        playerTypeStr: str = KlingonPower.Fair.name
        self.logger.info("playerTypeStr: %s", playerTypeStr)

        self.doTest(playerTypeStr, KlingonPower.Fair.value, "Fair value failed")

    def testGoodKlingonPower(self):
        playerTypeStr: str = KlingonPower.Good.name
        self.logger.info("playerTypeStr: %s", playerTypeStr)

        self.doTest(playerTypeStr, KlingonPower.Good.value, "Good value failed")

    def testExpertKlingonPower(self):
        playerTypeStr: str = KlingonPower.Expert.name
        self.logger.info("playerTypeStr: %s", playerTypeStr)

        self.doTest(playerTypeStr, KlingonPower.Expert.value, "Expert value failed")

    def testEmeritusKlingonPower(self):
        playerTypeStr: str = KlingonPower.Emeritus.name
        self.logger.info("playerTypeStr: %s", playerTypeStr)

        self.doTest(playerTypeStr, KlingonPower.Emeritus.value, "Emeritus value failed")

    def doTest(self, playerTypeStr, expectedValue, failMessage):

        klingonPowerValue: int = KlingonPower[playerTypeStr].value
        self.logger.info("klingonPowerValue: %s", klingonPowerValue)

        self.assertEqual(expectedValue, klingonPowerValue, failMessage)
