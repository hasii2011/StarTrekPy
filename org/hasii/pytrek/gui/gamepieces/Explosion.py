
import pygame
import os
import logging

from hasii.pytrek.gui.gamepieces.ExplosionColor import ExplosionColor
from hasii.pytrek.gui.gamepieces.GamePiece import GamePiece

class Explosion(GamePiece):
    """"""

    UPDATE_INTERVAL_SECONDS = 1

    def __init__(self, screen: pygame.Surface):
        """"""

        self.explosionColor = ExplosionColor.GREY
        filename            = "images/explosion_rays_{}.png".format(self.explosionColor.name.lower())
        super().__init__(screen, filename)

        self.soundExplosion = pygame.mixer.Sound(os.path.join('sounds', 'smallexplosion3.wav'))
        self.logger         = logging.getLogger(__name__)

        self.timeSinceLastExplosion = 0
        self.lastExplosion          = False
        self.currentPosition        = None

        self.soundExplosion.play()

    def update(self, sectorX: int, sectorY: int, playTime: float):
        """"""

        timeSinceLastUpdate = playTime - self.timeSinceLastExplosion
        #
        # Have we wrapped?
        #
        if self.explosionColor != ExplosionColor.NO_COLOR:

            super().update(sectorX, sectorY)
            if timeSinceLastUpdate > Explosion.UPDATE_INTERVAL_SECONDS:

                self.explosionColor = self.explosionColor.successor()
                self.logger.debug("Explosion Color %s", self.explosionColor.name)
                if self.explosionColor != ExplosionColor.NO_COLOR:
                    filename                    = "images/explosion_rays_{}.png".format(self.explosionColor.name.lower())
                    self.image                  = pygame.image.load(filename)
                    self.timeSinceLastExplosion = playTime
                    self.soundExplosion.play()
        else :
            self.logger.debug("Last Explosion occurred")
            self.lastExplosion = True
