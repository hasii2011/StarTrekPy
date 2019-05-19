#
#
#
import configparser
import os

from org.hasii.pytrek.GameMode import GameMode
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.GameType import GameType

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED   = (255,0,0)
DARK_BLUE = 0,0,128

class Settings:
    """
        A class to store all settings for this kewl game
        This class is a singleton
    """

    _singleton  = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(Settings)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):
        """Initialize the game's settings"""

        if self.__initialized == True:
            return
        else:
            self.__initialized = True

        self.screenWidth  = 800
        self.screenHeight = 700
        self.gameWidth    = 640
        self.gameHeight   = 640
        self.leftMargin   = 2
        self.bgColor      = BLACK
        self.rectColor    = BLACK
        #
        #
        #
        self.findConfigFile()
        config = configparser.ConfigParser()
        config.read("pyTrek.conf")

        self.maxStarCount    = config.getint('Limits','MaxStarCount')
        self.starBaseMinimum = config.getint("Limits", "StarBaseMinimum")
        self.starBaseMaximum = config.getint("Limits", "StarBaseMaximum")
        self.maxPlanets      = config.getint("Limits", "MaxPlanets")

        self.initialEnergyLevel   = config.getint('Power', 'InitialEnergyLevel')
        self.initialShieldEnergy  = config.getint('Power', 'InitialShieldEnergy')
        self.minimumImpulseEnergy = config.getint('Power', 'MinimumImpulseEnergy')

        self.gameLengthFactor     = config.getfloat("Factors", 'gameLengthFactor')
        self.starBaseExtender     = config.getfloat("Factors", "StarBaseExtender")
        self.starBaseMultiplier   = config.getfloat("Factors", "StarBaseMultiplier")

        skillStr                  = config.get("GameLevel", "PlayerSkill")
        self.skill                = PlayerType[skillStr]
        gameTypeStr               = config.get("GameLevel","GameType")
        self.gameType             = GameType[gameTypeStr]
        self.warpFactor           = config.getint("GameLevel", "DefaultWarpFactor")

        self.gameMode             = GameMode.Normal
        bogus = ''
    def findConfigFile(self):
        """"""
        # print("CurrentDir: " + os.getcwd())
        if os.path.isfile("pyTrek.conf"):
            return
        else:
            os.chdir("../")
            self.findConfigFile()

    def setGameMode(self, theGameMode: GameMode):
        """"""
        self.gameMode = theGameMode
    def getGameMode(self):
        """"""
        return self.gameMode