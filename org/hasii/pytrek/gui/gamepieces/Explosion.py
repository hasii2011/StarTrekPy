
import logging

import os

from pkg_resources import resource_filename

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
        # filename            = "images/explosion_rays_{}.png".format(self.explosionColor.name.lower())
        filename = f'explosion_rays_{self.explosionColor.name.lower()}.png'
        super().__init__(screen, filename)

        self.soundExplosion = pygame.mixer.Sound(os.path.join('sounds', 'smallexplosion3.wav'))
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
                    fqFileName: str = resource_filename(Settings.IMAGE_RESOURCES_PACKAGE_NAME, filename)

                    self.image:                  Surface = pygame.image.load(fqFileName)
                    self.timeSinceLastExplosion: float   = playTime
                    self.soundExplosion.play()
        else:
            self.logger.debug("Last Explosion occurred")
            self.lastExplosion = True
