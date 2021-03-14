
import json

import logging
from logging import Logger
from logging import getLogger

import logging.config

from pkg_resources import resource_filename

from os import chdir
from sys import path as sysPath

import pygame

from pygame import Surface

from albow.themes.ThemeLoader import ThemeLoader
from albow.themes.Theme import Theme

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.albow.StarTrekShell import StarTrekShell

JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"


class StarTrekPy:

    def __init__(self):
        # fqFileName = resource_filename(Settings.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)
        fqFileName: str = self._retrieveResourcePath(JSON_LOGGING_CONFIG_FILENAME)
        with open(fqFileName, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

        self.logger: Logger = getLogger(__name__)

        themeLoader: ThemeLoader = ThemeLoader()
        themeLoader.load()
        themeRoot: Theme = themeLoader.themeRoot
        Theme.setThemeRoot(themeRoot)

        self._settings: Settings = Settings()

        self._executionPath:  str = self._getExecutionPath()
        self.logger.warning(f'{self._executionPath=}')

    def run(self):
        pygame.init()
        pygame.display.set_caption("Star Trek ala' Python Albow")

        surface: Surface       = pygame.display.set_mode((self._settings.screenWidth, self._settings.screenHeight))
        shell:   StarTrekShell = StarTrekShell(surface)

        self._setOurSysPath()

        self.logger.info(f"Starting {__name__}")

        shell.run()

    def _getExecutionPath(self) -> str:
        """
        Return the absolute path currently used
        """
        absPath = sysPath[0]
        return absPath

    def _setOurSysPath(self):
        try:
            sysPath.append(self._executionPath)
            chdir(self._executionPath)
        except OSError as msg:
            self.logger.error(f"Error while setting path: {msg}")

    def _retrieveResourcePath(self, bareFileName: str) -> str:

        # Use this method in Python 3.9
        # from importlib_resources import files
        # configFilePath: str  = files('org.hasii.pytrek.resources').joinpath(JSON_LOGGING_CONFIG_FILENAME)

        try:
            fqFileName: str = resource_filename(Settings.RESOURCES_PACKAGE_NAME, bareFileName)
        except (ValueError, Exception):
            #
            # Maybe we are in an app
            #
            from os import environ
            print(f'In App')
            pathToResources: str = environ.get(f'{Settings.RESOURCE_ENV_VAR}')
            fqFileName:      str = f'{pathToResources}/{Settings.RESOURCES_PATH}/{bareFileName}'

        return fqFileName


if __name__ == "__main__":
    app: StarTrekPy = StarTrekPy()
    app.run()
