
import json

import logging
import logging.config

import pygame

from pygame import Surface

from albow.themes.ThemeLoader import ThemeLoader
from albow.themes.Theme import Theme

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.albow.StarTrekShell import StarTrekShell

JSON_LOGGING_CONFIG_FILENAME = "loggingConfiguration.json"


def main():

    with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
        configurationDictionary = json.load(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False

    logger = logging.getLogger(__name__)

    themeLoader: ThemeLoader = ThemeLoader()
    themeLoader.load()
    themeRoot: Theme = themeLoader.themeRoot
    Theme.setThemeRoot(themeRoot)

    settings: Settings = Settings()

    pygame.init()
    pygame.display.set_caption("Star Trek ala' Python Albow")

    surface: Surface = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    shell: StarTrekShell = StarTrekShell(surface)

    logger.info("Starting %s", __name__)

    shell.run()


if __name__ == "__main__":
    main()