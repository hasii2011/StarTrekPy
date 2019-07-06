
from typing import cast

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.GameType import GameType


class GameStatistics:
    """
    """

    _singleton  = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton               = object.__new__(GameStatistics)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):
        """"""
        if self.__initialized is True:
            return
        else:
            self._energy:              float = 0.0
            self._shieldEnergy:        float = 0.0
            self._starDate:            float = 0.0
            self._intime:              float = 0.0
            self._opTime:              float = 0.0  # #define Time a.Time time taken by current operation
            self._remainingGameTime:   float = 0.0
            self._remainingKlingons:   int   = 0
            self._remainingCommanders: int   = 0
            self._docked:              bool  = False

            self._skill:    PlayerType = cast(PlayerType, None)
            self._gameType: GameType   = cast(GameType, None)

            self.currentQuadrantCoordinates: Coordinates = cast(Coordinates, None)
            self.currentSectorCoordinates:   Coordinates = cast(Coordinates, None)

            self.gameActive:    bool = True
            self.__initialized: bool = True

    def getEnergy(self) -> float:
        return self._energy

    def setEnergy(self, theNewValue: float):
        self._energy = theNewValue

    def getShieldEnergy(self) -> float:
        return self._shieldEnergy

    def setShieldEnergy(self, theNewValue: float):
        self._shieldEnergy = theNewValue

    def getStarDate(self) -> float:
        return self._starDate

    def setStarDate(self, theNewValue: float):
        self._starDate = theNewValue

    def getInTime(self) -> float:
        return self._intime

    def setInTime(self, theNewValue: float):
        self._intime = theNewValue

    def getOpTime(self) -> float:
        return self._opTime

    def setOpTime(self, theNewValue: float):
        self._opTime = theNewValue

    def getRemainingGameTime(self) -> float:
        return self._remainingGameTime

    def setRemainingGameTime(self, theNewValue: float):
        self._remainingGameTime = theNewValue

    def getRemainingKlingons(self):
        return self._remainingKlingons

    def setRemainingKlingons(self, theNewValue: int):
        self._remainingKlingons = theNewValue

    def getRemainingCommanders(self):
        return self._remainingCommanders

    def setRemainingCommanders(self, theNewValue: int):
        self._remainingCommanders = theNewValue

    def getDocked(self) -> bool:
        return self._docked

    def setDocked(self, theNewValue: bool):
        self._docked = theNewValue

    def getSkill(self) -> PlayerType:
        return self._skill

    def setSkill(self, theNewValue: PlayerType):
        self._skill = theNewValue

    def getGameType(self) -> GameType:
        return self._gameType

    def setGameType(self, theNewValue: GameType):
        self._gameType = theNewValue

    def getCurrentQuadrantCoordinates(self) -> Coordinates:
        return self._currentQuadrantCoordinates

    def setCurrentQuadrantCoordinates(self, theNewValue: Coordinates):
        self._currentQuadrantCoordinates = theNewValue

    def getCurrentSectorCoordinates(self) -> Coordinates:
        return self._currentSectorCoordinates

    def setCurrentSectorCoordinates(self, theNewValue: Coordinates):
        self._currentSectorCoordinates = theNewValue

    shieldEnergy = property(getShieldEnergy, setShieldEnergy)
    energy       = property(getEnergy, setEnergy)
    intime       = property(getInTime, setInTime)
    opTime       = property(getOpTime, setOpTime)
    starDate     = property(getStarDate, setStarDate)

    remainingGameTime   = property(getRemainingGameTime,   setRemainingGameTime)
    remainingKlingons   = property(getRemainingKlingons,   setRemainingKlingons)
    remainingCommanders = property(getRemainingCommanders, setRemainingCommanders)
    docked              = property(getDocked,              setDocked)

    skill    = property(getSkill,    setSkill)
    gameType = property(getGameType, setGameType)

    currentQuadrantCoordinates = property(getCurrentQuadrantCoordinates, setCurrentQuadrantCoordinates)
    currentSectorCoordinates   = property(getCurrentSectorCoordinates,   setCurrentSectorCoordinates)

    def resetStatistics(self):
        self.gameActive = True

    def __repr__(self):
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
