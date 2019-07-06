
from typing import Dict

from logging import getLogger
from logging import Logger

from org.hasii.pytrek.GameStatistics import GameStatistics
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.Device import Device
from org.hasii.pytrek.engine.DeviceType import DeviceType

from org.hasii.pytrek.engine.futures.FutureEventType import FutureEventType
from org.hasii.pytrek.engine.futures.FutureEvent import FutureEvent


class EventEngine:

    _singleton: 'EventEngine' = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(EventEngine)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):

        if self.__initialized is True:
            return
        else:
            self.__initialized = True

        self.logger:       Logger         = getLogger(__name__)
        self.intelligence: Intelligence   = Intelligence()
        self.gameStats:    GameStatistics = GameStatistics()
        self.devices:      Devices        = Devices()

        self.eventMap: Dict[FutureEventType, FutureEvent] = {}
        for fsEventType in FutureEventType:
            if fsEventType != FutureEventType.FSPY:
                self.eventMap[fsEventType] = FutureEvent(fsEventType)

        self.eventMap[FutureEventType.FSNOVA]  = self.schedule(FutureEventType.FSNOVA,  self.intelligence.expRan(0.5 * self.gameStats.intime))
        self.eventMap[FutureEventType.FBATTAK] = self.schedule(FutureEventType.FBATTAK, self.intelligence.expRan(0.3 * self.gameStats.intime))

        self.logger.debug(f"eventMap: {self.eventMap}")

    def schedule(self, fEventType: FutureEventType, finTime: float) -> FutureEvent:

        retEvent: FutureEvent = FutureEvent(fEventType=fEventType, starDate=finTime)

        return retEvent

    def fixDevices(self):
        """
        // #define Time a.Time // time taken by current operation
        double fintim = d.date + Time
        datemin = fintim;

        // d.date is current stardate

        xtime = datemin-d.date;

        repair = xtime;

        /* Don't fix Deathray here */
        for (l=1; l<=ndevice; l++)
            if (damage[l] > 0.0 && l != DDRAY)
                damage[l] -= (damage[l]-repair > 0.0 ? repair : damage[l]);

        /* Fix Deathray if docked */
        if (damage[DDRAY] > 0.0 && condit == IHDOCKED)
            damage[DDRAY] -= (damage[l] - xtime > 0.0 ? xtime : damage[DDRAY]);

        /* If radio repaired, update star chart and attack reports */

        """
        fintim:  float = self.gameStats.starDate + self.gameStats.opTime
        datemin: float = fintim
        xtime:   float = datemin - self.gameStats.starDate
        repair:  float = xtime

        for devType in DeviceType:
            device: Device = self.devices.getDevice(devType)
            if device.deviceType != DeviceType.DeathRay:
                if device.damage > 0.0:
                    device.damage = device.damage - repair

        self.logger.info(f"Fixing Stuff")

    def __repr__(self):

        myRep = "\n"
        for dictKey, fsEvent in self.eventMap.items():
            devRep = (
                f"fsEvent: {fsEvent}\n"
            )
            myRep += devRep
        return myRep
