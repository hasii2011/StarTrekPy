
from typing import Dict
from typing import cast

from math import log

from random import randrange
from random import random

import logging
from logging import Logger
from logging import INFO

from org.hasii.pytrek.objects.Coordinates import Coordinates

from org.hasii.pytrek.engine.DeviceType import DeviceType
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus
from org.hasii.pytrek.engine.MoveBaddyData import MoveBaddyData

from org.hasii.pytrek.Settings import Settings


class Intelligence:
    """Is a smart piece of code"""

    _singleton    = None

    GALAXY_WIDTH            = 10
    GALAXY_HEIGHT           = 10
    QUADRANT_WIDTH          = 10
    QUADRANT_HEIGHT         = 10
    MIN_SECTOR_X_COORDINATE = 0
    MAX_SECTOR_X_COORDINATE = QUADRANT_HEIGHT - 1
    MIN_SECTOR_Y_COORDINATE = 0
    MAX_SECTOR_Y_COORDINATE = QUADRANT_WIDTH - 1

    MIN_QUADRANT_X_COORDINATE = 0
    MAX_QUADRANT_X_COORDINATE = GALAXY_WIDTH - 1
    MIN_QUADRANT_Y_COORDINATE = 0
    MAX_QUADRANT_Y_COORDINATE = GALAXY_HEIGHT - 1

    RANDOM_TIME_INTERVAL_START = 1.0
    RANDOM_TIME_INTERVAL_END   = 3.0  # end time is non-inclusive
    RANDOM_TIME_STEP           = 1.0

    RAND_MAX = 32767.0

    DAMAGE_WEIGHTS: Dict[DeviceType, float] = {
        DeviceType.ShortRangeSensors:   100,    # DSRSENS: short range scanners 10%
        DeviceType.LongRangeSensors:    100,    # DLRSENS: long range scanners 10%
        DeviceType.Phasers:             130,    # DPHASER: phasers 12%
        DeviceType.PhotonTubes:         135,    # DPHOTON: photon torpedoes 12%
        DeviceType.LifeSupport:         25,     # DLIFSUP: life support 2.5%
        DeviceType.WarpEngines:         65,     # DWARPEN: warp drive 6.5%
        DeviceType.ImpulseEngines:      70,     # DIMPULS: impulse engines 6.5%
        DeviceType.Shields:             145,    # DSHIELD: deflector shields 14.5%
        DeviceType.SubspaceRadio:       25,     # DRADIO:  subspace radio 2.5%
        DeviceType.ShuttleCraft:        5,      # DSHUTTL: shuttle 4.0%
        DeviceType.Computer:            15,     # DCOMPTR: computer 1.5%
        DeviceType.NavigationSystem:    20,     # NAVCOMP: navigation system 2.0%
        DeviceType.Transporter:         75,     # DTRANSP: transporter 7.5%
        DeviceType.ShieldControl:       20,     # DSHCTRL: high - speed shield controller 2.0%
        DeviceType.DeathRay:            1,      # DDRAY:   death ray 1.0%
        DeviceType.SpaceProbe:          5,      # DDSP:    deep - space probes 3.0%
        DeviceType.CAD:                 54      # DCAVD:   collision  avoidance 2.0%
    }

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(Intelligence)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):
        """"Constructor"""

        if self.__initialized is True:
            return
        else:
            self.__initialized = True

        self.settings: Settings = Settings()
        self.devices:  Devices  = Devices()
        self.logger:   Logger   = logging.getLogger(__name__)

        self.remainingKlingons = 0
        self.commanderCount    = 0

    def computeRandomTimeInterval(self) -> int:
        """
        Generate some random passage of time (stardates)
        """
        return randrange(self.RANDOM_TIME_INTERVAL_START, self.RANDOM_TIME_INTERVAL_END, self.RANDOM_TIME_STEP)

    def getRandomSectorCoordinates(self) -> Coordinates:
        """Generate a random set of sector coordinates"""

        x = randrange(self.QUADRANT_HEIGHT)
        y = randrange(self.QUADRANT_WIDTH)
        return Coordinates(x, y)

    def getRandomQuadrantCoordinates(self) -> Coordinates:
        """Generate a random set  of quadrant coordinates"""

        x = randrange(Intelligence.GALAXY_HEIGHT)
        y = randrange(Intelligence.GALAXY_WIDTH)
        return Coordinates(x, y)

    def getInitialStarBaseCount(self) -> int:
        """
                    Calculate and returns the star base count for the game start
            d.rembase = 3.0*Rand()+2.0;

            With the default values guarantees a minimum of 2 and a maximum of 5
        :return:  A starbase count
        """
        # retBaseCount = 0

        multiplier = self.settings.starBaseMultiplier
        extender   = self.settings.starBaseExtender
        # double rb = (3.0 * ourGPRandomGenerator.nextDouble()) + 2.0;
        nextDouble = random()
        self.logger.debug("nextDouble: %s", str(nextDouble))

        retBaseCount = (multiplier * nextDouble) + extender

        retBaseCount = round(retBaseCount)
        self.logger.info("calculated retBaseCount: %s", str(retBaseCount))

        minStarbaseCount = self.settings.starBaseMinimum
        maxStarbaseCount = self.settings.starBaseMaximum

        if retBaseCount < minStarbaseCount:
            retBaseCount = minStarbaseCount
            self.logger.info("adjusted retBaseCount: %s", str(retBaseCount))
        elif retBaseCount > maxStarbaseCount:
            retBaseCount = maxStarbaseCount
            self.logger.info("adjusted retBaseCount: %s", str(retBaseCount))

        return retBaseCount

    def getInitialKlingonCount(self, remainingGameTime: float) -> int:
        """

        private double      dremkl                  = 2.0*intime*((skill+1 - 2*Intelligence.Rand())*skill*0.1+0.15);

        public int myRemainingKlingons = (int) Math.round(dremkl);
        self.remainingKlingons = ((2.0 * self.remainingGameTime) * (self.skill.value + 1)) - (2 * nextNum) * (self.skill.value * 0.1) + 0.15

        :return:
        """
        nextNum = random() / 4.0
        self.logger.info(f"Random value: {nextNum}")

        self.remainingKlingons = (remainingGameTime * nextNum) + self.settings.skill.value + self.settings.gameType.value
        self.remainingKlingons = round(self.remainingKlingons)

        if self.logger.level == INFO:
            message = (
                f"Player Skill: '{self.settings.skill} "
                f"GameType '{self.settings.gameType}' "
                f"klingonCount: '{str(self.remainingKlingons)}'"
            )
            self.logger.info(message)

        return self.remainingKlingons

    def getInitialCommanderCount(self) -> int:
        """
        incom = skill + 0.0625*inkling*Rand();

        :return: Klingon Commander Count
        """

        assert hasattr(self, "remainingKlingons")
        self.commanderCount = self.settings.skill.value * 0.0625 * self.remainingKlingons * random()
        self.commanderCount = round(self.commanderCount)

        #
        # Adjust total Klingon count by # of commanders
        #
        self.remainingKlingons = self.remainingKlingons - self.commanderCount
        return self.commanderCount

    def getInitialGameTime(self) -> float:
        """"""
        if self.logger.level == INFO:
            msg = (
                f"Game Length factor: '{self.settings.gameLengthFactor}' "
                f"GameType: '{self.settings.gameType}' "
                f" GameTypeValue: '{self.settings.gameType.value}'"
            )
            self.logger.info(msg)
        remainingGameTime = self.settings.gameLengthFactor * self.settings.gameType.value
        return remainingGameTime

    def getInitialStarDate(self) -> int:

        starDate: int = int(100.0 * (31.0 * random()) * 20.0)
        return starDate

    def rand(self) -> float:
        """

        double Rand(void) {
            return rand()/(1.0 + (double)RAND_MAX);
        }

        Returns: Random float in range 0.0 - 0.99999

        """
        intermediateAns = randrange(start=0, stop=Intelligence.RAND_MAX)
        ans: float = intermediateAns / (1.0 + Intelligence.RAND_MAX)

        return ans

    def computeKlingonPower(self) -> float:
        """
        Regular klingon
            kpower[i] = Rand()*150.0 +300.0 +25.0*skill;

        Returns:

        """
        kPower: float = (self.rand() * 150.0) + 300.0 + (25.0 * self.settings.skill.value)
        return kPower

    def computeCommanderPower(self) -> float:
        """

        Commander
            kpower[klhere] = 950.0+400.0*Rand()+50.0*skill;

        Super Commander
            kpower[1] = 1175.0 + 400.0*Rand() + 125.0*skill;

        Returns:

        """
        cPower = 950.0 + (400.0 * self.rand()) + (50.0 * self.settings.skill.value)
        return cPower

    def expRan(self, avrage: float) -> float:
        """

        1e-7 -- 1 × 10 (minus 5) or 0.0000001
        double expran(double avrage) {
            return -avrage * log(1e-7 + Rand());
        }
        Returns:
        """
        return -avrage * log(1e-7 + self.rand())

    def isCriticalHit(self, theHitToCheck: float) -> bool:
        """

            if (hit < (275.0-25.0*game.skill)*(1.0+0.5* tk.rand()))
                return false;

        Args:
            theHitToCheck:

        Returns: _True_ if above the threshold, else _False_

        """
        threshHold: float = (275.0 - 25.0 * self.settings.skill.value) * (1.0 + 0.5 * self.rand())

        self.logger.info(f"theHitToCheck: {theHitToCheck} playerSkill: {self.settings.skill} threshHold: {threshHold}")
        ans = False
        if theHitToCheck > threshHold:
            ans = True
        return ans

    def fryDevice(self, theHit: float) -> DeviceType:
        """
        ncrit = 1.0 + hit/(500.0+100.0*tk.rand());

         extradm = (hit * game.damfac) / (ncrit * (75.0+25.0 * tk.rand()));

       // Select devices and cause damage
        for (int loop1 = 0; loop1 < ncrit; loop1++) {
            do {
                j = randdevice();
                // Cheat to prevent shuttle damage unless on ship
            } while (game.damage[j]<0.0 || (j==DSHUTTL && (game.iscraft != IsCraft.onship)));
            cdam[loop1] = j;
            damaged [j] = 1;

        Args:
            theHit:

        Returns:

        """

        damagedDeviceType: DeviceType = cast(DeviceType, None)
        if self.isCriticalHit(theHit) is True:

            ncrit:    float = 1.0 + theHit / (500.0 + 100.0 * self.rand())
            ncritInt: int   = round(ncrit)
            x = 0
            while x < ncritInt:
                damagedDeviceType = self._getRandomDevice()
                x += 1
            extradm: float = (theHit * self.settings.damageFactor) / (ncrit * (75.0 + 25.0 * self.rand()))

            # TODO Prevent shuttle damage unless on ship
            self.devices.setDeviceStatus(deviceType=damagedDeviceType, deviceStatus=DeviceStatus.Damaged)
            currentDamage: float = self.devices.getDeviceDamage(damagedDeviceType)
            currentDamage += extradm
            self.devices.setDeviceDamage(deviceType=damagedDeviceType, damageValue=currentDamage)

        return damagedDeviceType

    def moveBaddy(self, moveBaddyData: MoveBaddyData, baddyLocation: Coordinates):
        """
        loccom:

        Args:
            moveBaddyData: Additional information we need from the game

            baddyLocation: quadrant location for commander or super commander

        Returns:

        """

        comX: int = baddyLocation.x
        comY: int = baddyLocation.y
        self.logger.info(f"comX: {comX}, comY: {comY}")
        # This should probably be just comhere + ishere
        # int nbaddys = skill > SGOOD ? (int)((comhere * 2 + ishere * 2 + klhere * 1.23 + irhere * 1.5) / 2.0): (comhere + ishere);
        # ishere  - super commander in quadrant
        # comhere - commanders in quadrant
        # klhere  - klingons in quadrant
        # irhere  - Romulans in quadrant

        klhere:  int = moveBaddyData.numberOfKlingons
        comhere: int = moveBaddyData.numberOfCommanders
        ishere:  int = moveBaddyData.numberOfSuperCommanders
        irhere:  int = moveBaddyData.numberOfRomulans

        skill:   PlayerType = moveBaddyData.playerSkill

        if skill.value > PlayerType.Good.value:
            nbaddys: int = round((comhere * 2 + ishere * 2 + klhere * 1.23 + irhere * 1.5) / 2.0)
        else:
            nbaddys: int = comhere + ishere
        self.logger.info(f"nbaddys: {nbaddys}")

    def _getRandomDevice(self) -> DeviceType:
        """
        Use the algorithm from SpaceWar

            int sum = 0;
            int idx = (int) Math.round (tk.rand() * 1000.0);    /* weights must sum to 1000 */

            for (int i = 0; i < Constants.NDEVICES; i++) {
                sum += weights[i];
                if (idx < sum)
                    return i;
            }

            return Constants.NDEVICES -1;   // we should never get here, but I have seen it happen

        Returns: A random devices

        """
        runningWeight: int = 0
        weightToBeat:  int = int(round(self.rand() * 1000.0))

        self.logger.debug(f"weightToBeat: {weightToBeat}")
        randomDevice: DeviceType = cast(DeviceType, None)
        for deviceType in DeviceType:
            weight = Intelligence.DAMAGE_WEIGHTS[deviceType]
            runningWeight += weight
            if weightToBeat < runningWeight:
                randomDevice = deviceType
                break
        #
        # May return `None` as original code occasionally failed
        # fails about 1 in every 2500 calls
        #
        if randomDevice is None:
            self.logger.error("Code fail, make up for it")
            randomDevice = DeviceType.CAD

        return randomDevice
