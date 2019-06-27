
import logging

import pygame

from pygame import Surface

from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece

from org.hasii.pytrek.gui.gamepieces.BasicTorpedo import BasicTorpedo

from org.hasii.pytrek.objects.Coordinates import Coordinates


class KlingonTorpedo(BasicTorpedo):

    def __init__(self, screen: Surface, shooterPower: float, shooterPosition: Coordinates):
        """

        Args:
            screen:             pygame place to draw
            shooterPower:       The shooter's power
            shooterPosition:    The shooter's position
        """

        super().__init__(screen, "images/KlingonTorpedo.png")

        self.logger                       = logging.getLogger(__name__)
        self.followerImage:   Surface     = pygame.image.load('images/KlingonTorpedoFollower-16.png')
        self.shooterPower:    float       = shooterPower
        self.shooterPosition: Coordinates = shooterPosition

        self.prevDebugIdx = 0
        self.idxChecked   = False

    def update(self, sectorX: int, sectorY: int, playTime: float = 0):

        super().update(sectorX, sectorY, playTime)

        followerIdx = self.currentTrajectoryIdx - 1
        self.showFollower(followerIdx)

    def showFollower(self, followerIdx: int):

        self._debugFollower(followerIdx)
        if followerIdx >= 0:
            self._debugFollower(followerIdx)
            if self.torpedoAtTarget is False:
                sectorX: int = self.trajectory[followerIdx].getX()
                sectorY: int = self.trajectory[followerIdx].getY()
                self.blitImage(sectorX, sectorY, self.followerImage)
                self.showFollower(followerIdx - 1)

    def blitImage(self, sectorX: int, sectorY: int, imageToBlit: Surface):

        self.rect.x = ((sectorX * GamePiece.MEDIUM_SPRITE_WIDTH)  * 4) + GamePiece.MEDIUM_X_ADJUSTMENT + self.settings.leftMargin
        self.rect.y = ((sectorY * GamePiece.MEDIUM_SPRITE_HEIGHT) * 4) + GamePiece.MEDIUM_Y_ADJUSTMENT

        self.logger.debug(f"sectorX: {str(sectorX)} self.rect.x: {str(self.rect.x)} sectorY: {str(sectorY)} self.rect.y: {str(self.rect.y)}")
        self.logger.debug(str(self.rect))
        self.screen.blit(imageToBlit, self.rect)

    def _debugFollower(self, fIdx):
        if self.logger.level == logging.DEBUG:
            if self.prevDebugIdx != fIdx and self.idxChecked is False:
                currentTrajectoryIdx = self.currentTrajectoryIdx
                currentFollowerLoc      = self.trajectory[fIdx]
                self.logger.info(f"followerIdx: {fIdx} - currentTrajectoryIdx: '{currentTrajectoryIdx}' Follower at: '{currentFollowerLoc}'")
                self.idxChecked = True
            else:
                self.prevDebugIdx = fIdx
                self.idxChecked = False
