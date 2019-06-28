
from math import log

from random import randrange

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.Settings import Settings

from random import random

import logging


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

        self.settings = Settings()
        self.logger   = logging.getLogger(__name__)

        self.gameType = self.settings.gameType
        self.skill    = self.settings.skill

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
        self.logger.info("Random value: %s", nextNum)

        self.remainingKlingons = (remainingGameTime * nextNum) + self.skill.value + self.gameType.value
        self.remainingKlingons = round(self.remainingKlingons)

        self.logger.info("Player Skill: '%s', GameType '%s', klingonCount: %s",
                         self.skill.name, self.gameType.name, str(self.remainingKlingons))

        return self.remainingKlingons

    def getInitialCommanderCount(self) -> int:
        """
        incom = skill + 0.0625*inkling*Rand();

        :return: Klingon Commander Count
        """

        assert hasattr(self, "remainingKlingons")
        self.commanderCount = self.skill.value * 0.0625 * self.remainingKlingons * random()
        self.commanderCount = round(self.commanderCount)

        #
        # Adjust total Klingon count by # of commanders
        #
        self.remainingKlingons = self.remainingKlingons - self.commanderCount
        return self.commanderCount

    def getInitialGameTime(self) -> float:
        """"""
        self.logger.info("Game Length factor: '%s'  GameType: '%s' GameTypeValue: '%s'",
                         self.settings.gameLengthFactor, self.gameType.name, self.gameType.value)
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
        kPower: float = (self.rand() * 150.0) + 300.0 + (25.0 * self.skill.value)
        return kPower

    def computeCommanderPower(self) -> float:
        """

        Commander
            kpower[klhere] = 950.0+400.0*Rand()+50.0*skill;

        Super Commander
            kpower[1] = 1175.0 + 400.0*Rand() + 125.0*skill;

        Returns:

        """
        cPower = 950.0 + (400.0 * self.rand()) + (50.0 * self.skill.value)
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
