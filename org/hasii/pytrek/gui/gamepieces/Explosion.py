
import logging

import pygame

from pygame import Surface

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.gui.gamepieces.ExplosionColor import ExplosionColor
from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece


class Explosion(GamePiece):
    """"""

    UPDATE_INTERVAL_SECONDS = 1

    def __init__(self, screen: pygame.Surface):
        """"""

        self.explosionColor = ExplosionColor.GREY

        filename = f'explosion_rays_{self.explosionColor.name.lower()}.png'
        super().__init__(screen, filename)

        fqFileName: str = Settings.getResourcesPath(bareFileName='SmallExplosion.wav',
                                                    resourcePackageName=Settings.SOUND_RESOURCES_PACKAGE_NAME,
                                                    resourcesPath=Settings.SOUND_RESOURCES_PATH
                                                    )

        self.soundExplosion = pygame.mixer.Sound(fqFileName)
        self.logger         = logging.getLogger(__name__)

        self.timeSinceLastExplosion = 0
        self.lastExplosion          = False
        self.currentPosition        = None

        self.soundExplosion.play()

    def update(self, sectorX: int, sectorY: int, playTime: float = 0):
        """"""

        timeSinceLastUpdate = playTime - self.timeSinceLastExplosion
        #
        # Have we wrapped?
        #
        if self.explosionColor != ExplosionColor.NO_COLOR:

            super().update(sectorX, sectorY)
            if timeSinceLastUpdate > Explosion.UPDATE_INTERVAL_SECONDS:

                self.explosionColor = self.explosionColor.successor()
                self.logger.debug(f'Explosion Color {self.explosionColor.name}')

                if self.explosionColor != ExplosionColor.NO_COLOR:

                    filename:   str = f'explosion_rays_{self.explosionColor.name.lower()}.png'

                    fqFileName: str = Settings.getResourcesPath(bareFileName=filename,
                                                                resourcePackageName=Settings.IMAGE_RESOURCES_PACKAGE_NAME,
                                                                resourcesPath=Settings.IMAGE_RESOURCES_PATH
                                                                )

                    self.image:                  Surface = pygame.image.load(fqFileName)
                    self.timeSinceLastExplosion: float   = playTime
                    self.soundExplosion.play()
        else:
            self.logger.debug("Last Explosion occurred")
            self.lastExplosion = True
