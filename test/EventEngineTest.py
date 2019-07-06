
import logging

from logging import Logger

from BaseTest import BaseTest

from org.hasii.pytrek.engine.GameEngine import GameEngine

from org.hasii.pytrek.engine.futures.EventEngine import EventEngine


class EventEngineTest(BaseTest):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger:      Logger      = logging.getLogger(__name__)
        #
        # The game engine initializes the game stats object (for better or worse)
        #
        self.gameEngine:  GameEngine  = GameEngine()
        self.eventEngine: EventEngine = EventEngine()

    def testEventEngineIsSingleton(self):

        eventEngine: EventEngine = EventEngine()

        self.logger.info(f"eventEngine: {eventEngine}")

        doppleGangerEngine: EventEngine = EventEngine()
        self.logger.info(f"doppleGangerEngine: {doppleGangerEngine}")

        self.assertEqual(first=eventEngine, second=doppleGangerEngine, msg="Not a singleton")

    def testFixDevices(self):

        travelDistance: float = 3.162222
        warpFactor:     float = 5.0
        warpSquared: float = warpFactor ** 2
        elapsedTime: float = 10.0 * travelDistance / warpSquared
        self.gameEngine.stats.opTime = elapsedTime

        self.eventEngine.fixDevices()
