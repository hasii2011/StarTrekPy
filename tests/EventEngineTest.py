
import logging

from logging import Logger

from BaseTest import BaseTest

from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.Device import Device
from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus
from org.hasii.pytrek.engine.DeviceType import DeviceType

from org.hasii.pytrek.engine.futures.EventEngine import EventEngine

BASIC_DAMAGE = 4.0


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
        self.devices:     Devices     = Devices()

    def testEventEngineIsSingleton(self):

        eventEngine: EventEngine = EventEngine()

        self.logger.info(f"eventEngine: {eventEngine}")

        doppleGangerEngine: EventEngine = EventEngine()
        self.logger.info(f"doppleGangerEngine: {doppleGangerEngine}")

        self.assertEqual(first=eventEngine, second=doppleGangerEngine, msg="Not a singleton")

    def testFixDevices(self):

        self.devices.getDevice(DeviceType.Phasers).damage       = BASIC_DAMAGE
        self.devices.getDevice(DeviceType.Phasers).deviceStatus = DeviceStatus.Damaged

        travelDistance: float = 3.162222
        warpFactor:     float = 5.0
        warpSquared: float = warpFactor ** 2
        elapsedTime: float = 10.0 * travelDistance / warpSquared
        self.gameEngine.stats.opTime = elapsedTime

        self.eventEngine.fixDevices()

        repairedValue: float = BASIC_DAMAGE - elapsedTime

        repairedDevice: Device = self.devices.getDevice(DeviceType.Phasers)
        updatedFix:     float  = repairedDevice.getDamage()

        self.assertAlmostEqual(first=repairedValue, second=updatedFix, msg="Not enough repair")

    def testFixDevicesNoOpTime(self):

        self.gameEngine.stats.opTime = 0.0
        self.devices.getDevice(DeviceType.PhotonTubes).damage       = BASIC_DAMAGE
        self.devices.getDevice(DeviceType.PhotonTubes).deviceStatus = DeviceStatus.Damaged

        self.eventEngine.fixDevices()

        repairedDevice: Device = self.devices.getDevice(DeviceType.PhotonTubes)
        updatedFix:     float  = repairedDevice.getDamage()

        self.assertEqual(first=BASIC_DAMAGE, second=updatedFix, msg="Should not have been repaired")
        self.logger.info(f"updatedFix: {updatedFix}")
