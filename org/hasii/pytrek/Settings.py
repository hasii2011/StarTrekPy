
import configparser

from os import sep as osSep

from pkg_resources import resource_filename

from org.hasii.pytrek.GameMode import GameMode
from org.hasii.pytrek.engine.PlayerType import PlayerType
from org.hasii.pytrek.engine.GameType import GameType

from albow.core.ui.AlbowEventLoop import AlbowEventLoop

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
DARK_BLUE = (0, 0, 128)


class Settings:
    """
        A class to store all settings for this kewl game
        This class is a singleton
    """
    RESOURCE_ENV_VAR:             str = 'RESOURCEPATH'
    RESOURCES_PACKAGE_NAME:       str = 'org.hasii.pytrek.resources'
    FONT_RESOURCES_PACKAGE_NAME:  str = 'org.hasii.pytrek.resources.fonts'
    IMAGE_RESOURCES_PACKAGE_NAME: str = 'org.hasii.pytrek.resources.images'
    SOUND_RESOURCES_PACKAGE_NAME: str = 'org.hasii.pytrek.resources.sounds'

    RESOURCES_PATH:       str = 'org/hasii/pytrek/resources'
    SOUND_RESOURCES_PATH: str = f'{RESOURCES_PATH}{osSep}sounds'
    IMAGE_RESOURCES_PATH: str = f'{RESOURCES_PATH}{osSep}images'
    FONT_RESOURCES_PATH:  str = f'{RESOURCES_PATH}{osSep}fonts'

    SETTINGS_FILENAME: str = 'pyTrek.conf'

    FIXED_WIDTH_FONT_NAME:           str = 'MonoFonto.ttf'
    ALTERNATE_FIXED_WIDTH_FONT_NAME: str = 'FuturistFixedWidth.ttf'

    CLOCK_EVENT           = AlbowEventLoop.MUSIC_END_EVENT + 1
    KLINGON_TORPEDO_EVENT = CLOCK_EVENT + 1
    GAME_OVER_EVENT       = KLINGON_TORPEDO_EVENT + 1
    ENTERPRISE_HIT_BY_TORPEDO_EVENT = GAME_OVER_EVENT + 1

    DEFAULT_FULL_SHIELDS = 2500.0

    _singleton  = None

    def __new__(cls, *args, **kwargs):

        if not cls._singleton:
            cls._singleton = object.__new__(Settings)
            cls._singleton.__initialized = False
        return cls._singleton

    def __init__(self):
        """Initialize the game's settings"""

        if self.__initialized is True:
            return
        else:
            self.__initialized = True

        self.screenWidth  = 800
        self.screenHeight = 700 + 130
        self.gameWidth    = 640
        self.gameHeight   = 640
        self.leftMargin   = 2
        self.bgColor      = BLACK
        self.rectColor    = BLACK
        #
        #
        #
        fqFileName: str = Settings.getResourcesPath(resourcePackageName=Settings.RESOURCES_PACKAGE_NAME,
                                                    resourcesPath=Settings.RESOURCES_PATH,
                                                    bareFileName=Settings.SETTINGS_FILENAME
                                                    )
        config = configparser.ConfigParser()
        config.read(fqFileName)

        self.maxStarCount    = config.getint('Limits', 'MaxStarCount')
        self.starBaseMinimum = config.getint("Limits", "StarBaseMinimum")
        self.starBaseMaximum = config.getint("Limits", "StarBaseMaximum")
        self.maxPlanets      = config.getint("Limits", "MaxPlanets")

        self.initialEnergyLevel   = config.getint('Power', 'InitialEnergyLevel')
        self.initialShieldEnergy  = config.getint('Power', 'InitialShieldEnergy')
        self.minimumImpulseEnergy = config.getint('Power', 'MinimumImpulseEnergy')
        self.initialTorpedoCount  = config.getint('Power',  'InitialTorpedoCount')

        self.gameLengthFactor     = config.getfloat("Factors", 'gameLengthFactor')
        self.starBaseExtender     = config.getfloat("Factors", "StarBaseExtender")
        self.starBaseMultiplier   = config.getfloat("Factors", "StarBaseMultiplier")

        skillStr                  = config.get("GameLevel", "PlayerSkill")
        self.skill                = PlayerType[skillStr]
        gameTypeStr               = config.get("GameLevel", "GameType")
        self.gameType             = GameType[gameTypeStr]
        self.warpFactor           = config.getint("GameLevel", "DefaultWarpFactor")

        #     game.damfac = 0.5 * game.skill;
        self.damageFactor = 0.5 * self.skill.value
        self.gameMode     = GameMode.Normal

    def setGameMode(self, theGameMode: GameMode):
        """"""
        self.gameMode = theGameMode

    def getGameMode(self):
        """"""
        return self.gameMode

    @staticmethod
    def getResourcesPath(resourcePackageName: str, resourcesPath: str, bareFileName: str) -> str:

        try:
            fqFileName: str = resource_filename(resourcePackageName, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            pathToResources: str = environ.get(f'{Settings.RESOURCE_ENV_VAR}')
            fqFileName:      str = f'{pathToResources}/{resourcesPath}/{bareFileName}'

        return fqFileName
