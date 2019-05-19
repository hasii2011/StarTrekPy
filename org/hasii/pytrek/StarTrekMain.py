import logging
import logging.config

import pygame

from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.gui.GameLoop import GameLoop

def runGame():

    logging.config.fileConfig('logging.conf')

    logger   = logging.getLogger(__name__)
    settings = Settings()
    pygame.init()                               # initialize pygame
    screen   = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
    pygame.display.set_caption("Star Trek ala' Python")
    pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag

    screenRect = screen.get_rect()

    logger.info("right: %s, bottom; %s, extended image support; %s",
                str(screenRect.right),
                str(screenRect.bottom),
                bool(pygame.image.get_extended())
          )

    FPS       = 30
    clock     = pygame.time.Clock()
    playTime  = 0
    cycleTime = 0
    gameLoop  = GameLoop(screen=screen)

    pygame.time.set_timer(GameLoop.CLOCK_EVENT, 10 * 1000)
    pygame.time.set_timer(GameLoop.KLINGON_TORPEDO_EVENT, 15 * 1000)

    while True:

        gameLoop.checkPyGameEvents()
        gameLoop.updateScreen(playTime=playTime)

        milliseconds = clock.tick(FPS)        # milliseconds passed since last frame
        seconds      = milliseconds / 1000.0  # seconds passed since last frame (float)
        playTime     += seconds
        cycleTime    += seconds

        if cycleTime > 10:
            # logger.debug("10 seconds have elapsed")
            cycleTime = 0
#
#
#
if __name__ == "__main__":
    runGame()