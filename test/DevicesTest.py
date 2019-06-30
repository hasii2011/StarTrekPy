
import logging
import unittest

from BaseTest import BaseTest

from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.Device import Device
from org.hasii.pytrek.engine.DeviceType import DeviceType
from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus


class DevicesTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger = logging.getLogger(__name__)

    def testDevicesClassISingleton(self):

        devices: Devices = Devices()

        self.logger.info(f"devices: {devices}")

        doppleGangerDevices: Devices = Devices()
        self.logger.info(f"doppleGangerDevices: {doppleGangerDevices}")

        self.assertEqual(first=devices, second=doppleGangerDevices, msg="Not a singleton")

    def testGetDevice(self):

        devices: Devices = Devices()

        testDevice: Device = devices.getDevice(DeviceType.DeathRay)

        self.assertEqual(first=testDevice.deviceType, second=DeviceType.DeathRay, msg='Got wrong device')

    def testSetDeviceStatus(self):

        devices: Devices = Devices()
        devices.setDeviceStatus(deviceType=DeviceType.LifeSupport, deviceStatus=DeviceStatus.Damaged)

        lifeSupport: Device = devices.getDevice(DeviceType.LifeSupport)

        self.assertEqual(first=lifeSupport.deviceStatus, second=DeviceStatus.Damaged, msg='Device did not change status')

        devices.setDeviceStatus(deviceType=DeviceType.LifeSupport, deviceStatus=DeviceStatus.Down)

        lf2: Device = devices.getDevice(DeviceType.LifeSupport)

        self.assertEqual(first=lf2.deviceStatus, second=DeviceStatus.Down, msg='Status did not change')


if __name__ == '__main__':
    unittest.main()
