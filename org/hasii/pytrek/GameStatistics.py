from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.GameType import GameType
from org.hasii.pytrek.engine.ShieldStatus import ShieldStatus
from org.hasii.pytrek.engine.TorpedoStatus import TorpedoStatus
from org.hasii.pytrek.engine.PhaserStatus import PhaserStatus
from org.hasii.pytrek.engine.ComputerStatus import ComputerStatus

class GameStatistics:

    _singleton  = None
    gameActive  = True

    skill:               PlayerType
    gameType:            GameType
    energy:              float
    shieldEnergy:        float
    starDate:            float
    remainingGameTime:   float
    remainingKlingons:   float
    remainingCommanders: float

    currentQuadrantCoordinates: Coordinates
    currentSectorCoordinates:   Coordinates

    shieldStatus:   ShieldStatus   = ShieldStatus.Up
    torpedoStatus:  TorpedoStatus  = TorpedoStatus.Up
    phaserStatus:   PhaserStatus   = PhaserStatus.Up
    computerStatus: ComputerStatus = ComputerStatus.Up


    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton               = object.__new__(GameStatistics)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):
        """"""
        if self.__initialized == True:
            return
        else:
            self.__initialized = True

        self.gameActive = True

    def resetStatistics(self):
        self.gameActive = True

    def __repr__(self):
        return '<%s at %s>' % (self.__class__.__name__, hex(id(self)))
        # return '%s' % (hex(id(self)))
