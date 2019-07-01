
import logging

from logging import Logger

from org.hasii.pytrek.engine.DeviceType import DeviceType
from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus


class Device:

    def __init__(self, deviceType: DeviceType, deviceStatus: DeviceStatus, initialDamage: float = 0.0):

        self.logger: Logger = logging.getLogger(__name__)

        self._deviceType:   DeviceType   = deviceType
        self._deviceStatus: DeviceStatus = deviceStatus
        self._damage:       float        = initialDamage

    def getDeviceType(self) -> DeviceType:
        return self._deviceType

    def setDeviceType(self, theNewValue: DeviceType):
        self._deviceType = theNewValue

    def getDeviceStatus(self) -> DeviceStatus:
        return self._deviceStatus

    def setDeviceStatus(self, theNewValue: DeviceStatus):
        self._deviceStatus = theNewValue

    def getDamage(self) -> float:
        return self._damage

    def setDamage(self, theNewValue: float):
        self._damage = theNewValue

    deviceType   = property(getDeviceType, setDeviceType)
    deviceStatus = property(getDeviceStatus, setDeviceStatus)
    damage       = property(getDamage, setDamage)

    def __repr__(self):

        myRep = f"deviceType: {self.deviceType} deviceStatus: {self.deviceStatus} damage: {self.damage}"
        return myRep
