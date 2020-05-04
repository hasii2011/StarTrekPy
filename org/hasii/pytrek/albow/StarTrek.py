
import json

import logging
from logging import Logger
from logging import getLogger

import logging.config

from pkg_resources import resource_filename

import pygame

from pygame import Surface

from albow.themes.ThemeLoader import ThemeLoader
from albow.themes.Theme import Theme

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.albow.StarTrekShell import StarTrekShell

JSON_LOGGING_CONFIG_FILENAME: str = "loggingConfiguration.json"


class StarTrekPy:

    def __init__(self):
        fqFileName = resource_filename(Settings.RESOURCES_PACKAGE_NAME, JSON_LOGGING_CONFIG_FILENAME)

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

    def run(self):
        pygame.init()
        pygame.display.set_caption("Star Trek ala' Python Albow")

        surface: Surface = pygame.display.set_mode((self._settings.screenWidth, self._settings.screenHeight))
        shell: StarTrekShell = StarTrekShell(surface)

        self.logger.info(f"Starting {__name__}")

        shell.run()


if __name__ == "__main__":
    app: StarTrekPy = StarTrekPy()
    app.run()
