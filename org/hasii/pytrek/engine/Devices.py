
from typing import Dict

import logging

from org.hasii.pytrek.engine.Device import Device
from org.hasii.pytrek.engine.DeviceType import DeviceType
from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus


class Devices:

    _singleton: 'Devices'    = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(Devices)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):

        if self.__initialized is True:
            return
        else:
            self.__initialized = True

        self.logger =  logging.getLogger(__name__)

        self.deviceMap: Dict[DeviceType, Device] = {}

        for deviceType in DeviceType:

            device: Device = Device(deviceType=deviceType, deviceStatus=DeviceStatus.Up)
            self.deviceMap[deviceType] = device

        self.logger.info(f"Created {len(self.deviceMap):3} devices")

    def getDevice(self, deviceType: DeviceType):

        self.logger.info(f"deviceType: {deviceType}")
        return self.deviceMap[deviceType]

    def setDeviceStatus(self, deviceType: DeviceType, deviceStatus: DeviceStatus):

        self.logger.info(f"deviceType: {deviceType}, deviceStatus: {deviceStatus}")
        self.deviceMap[deviceType].deviceStatus = deviceStatus

    def setDeviceDamage(self, deviceType: DeviceType, damageValue: float):

        self.logger.info(f"deviceType: {deviceType}, damageValue: {damageValue}")
        self.deviceMap[deviceType].damage = damageValue

    def __repr__(self):

        myRep = "\n"
        for deviceType, device in self.deviceMap.items():
            devRep = (
                f"deviceType: {deviceType:27} "
                f"deviceStatus: {device.deviceStatus:7} "
                f"damage: {device.damage:4.4} \n"
            )
            myRep += devRep
        return myRep
