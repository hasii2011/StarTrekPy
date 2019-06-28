
import logging

from logging import Logger

from typing import cast

from org.hasii.pytrek.engine.DeviceType import DeviceType


class Device:

    def __init__(self):

        self.logger: Logger = logging.getLogger(__name__)

        self.deviceType:  DeviceType = cast(DeviceType, None)
        self.damageValue: float      = 0.0
