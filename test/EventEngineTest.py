
import logging

from logging import Logger

from BaseTest import BaseTest

from hasii.pytrek.engine.futures.EventEngine import EventEngine


class EventEngineTest(BaseTest):
    """"""
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger:      Logger      = logging.getLogger(__name__)
        self.eventEngine: EventEngine = EventEngine()

    def testEventEngineISingleton(self):

        eventEngine: EventEngine = EventEngine()

        self.logger.info(f"eventEngine: {eventEngine}")

        doppleGangerEngine: EventEngine = EventEngine()
        self.logger.info(f"doppleGangerEngine: {doppleGangerEngine}")

        self.assertEqual(first=eventEngine, second=doppleGangerEngine, msg="Not a singleton")
