
from typing import cast

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.GameType import GameType
from org.hasii.pytrek.engine.ShieldStatus import ShieldStatus
from org.hasii.pytrek.engine.TorpedoStatus import TorpedoStatus
from org.hasii.pytrek.engine.PhaserStatus import PhaserStatus
from org.hasii.pytrek.engine.ComputerStatus import ComputerStatus


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
            self._energy:             float = 0.0
            self._shieldEnergy:       float = 0.0
            self._starDate:           float = 0.0
            self._remainingGameTime:  float = 0.0
            self._remainingKlingons:   int   = 0
            self._remainingCommanders: int   = 0

            self._skill:    PlayerType = cast(PlayerType, None)
            self._gameType: GameType   = cast(GameType, None)

            self._shieldStatus:   ShieldStatus   = ShieldStatus.Up
            self._torpedoStatus:  TorpedoStatus  = TorpedoStatus.Up
            self._phaserStatus:   PhaserStatus   = PhaserStatus.Up
            self._computerStatus: ComputerStatus = ComputerStatus.Up

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

    def getRemainingGameTime(self):
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

    def getSkill(self) -> PlayerType:
        return self._skill

    def setSkill(self, theNewValue: PlayerType):
        self._skill = theNewValue

    def getGameType(self) -> GameType:
        return self._gameType

    def setGameType(self, theNewValue: GameType):
        self._gameType = theNewValue

    def getShieldStatus(self) -> ShieldStatus:
        return self._shieldStatus

    def setShieldStatus(self, theNewValue: ShieldStatus):
        self._shieldStatus = theNewValue

    def getTorpedoStatus(self) -> TorpedoStatus:
        return self._torpedoStatus

    def setTorpedoStatus(self, theNewValue: TorpedoStatus):
        self._torpedoStatus = theNewValue

    def getPhaserStatus(self) -> PhaserStatus:
        return self._phaserStatus

    def setPhaserStatus(self, theNewValue: PhaserStatus):
        self._phaserStatus = theNewValue

    def getComputerStatus(self) -> ComputerStatus:
        return self._computerStatus

    def setComputerStatus(self, theNewValue: ComputerStatus):
        self._computerStatus = theNewValue

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
    starDate     = property(getStarDate, setStarDate)

    remainingGameTime   = property(getRemainingGameTime,  setRemainingGameTime)
    remainingKlingons   = property(getRemainingKlingons,  setRemainingKlingons)
    remainingCommanders = property(getRemainingCommanders, setRemainingCommanders)

    skill    = property(getSkill,    setSkill)
    gameType = property(getGameType, setGameType)

    shieldStatus    = property(getShieldStatus,   setShieldStatus)
    torpedoStatus   = property(getTorpedoStatus,  setTorpedoStatus)
    phaserStatus    = property(getPhaserStatus,   setPhaserStatus)
    computerStatus  = property(getComputerStatus, setComputerStatus)

    currentQuadrantCoordinates = property(getCurrentQuadrantCoordinates, setCurrentQuadrantCoordinates)
    currentSectorCoordinates   = property(getCurrentSectorCoordinates,   setCurrentSectorCoordinates)

    def resetStatistics(self):
        self.gameActive = True

    def __repr__(self):
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
