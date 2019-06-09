
from pygame import Surface

import logging

from org.hasii.pytrek.gui.GamePiece import GamePiece


class BasicTorpedo(GamePiece):
    """"""

    UPDATE_INTERVAL_SECONDS = 1

    def __init__(self, screen: Surface, fileName: str):
        """"""

        super().__init__(screen, fileName)

        self.logger = logging.getLogger(__name__)

        self.currentTrajectoryIdx = 0
        self.trajectory           = []
        self.timeSinceMovement    = 0
        self.torpedoAtTarget      = False

    def update(self, sectorX: int, sectorY: int, playTime: float = 0):
        """"""

        timeSinceLastUpdate = playTime - self.timeSinceMovement

        if self.currentTrajectoryIdx < self.trajectory.__len__() - 1:

            if timeSinceLastUpdate > BasicTorpedo.UPDATE_INTERVAL_SECONDS:

                self.currentTrajectoryIdx += 1
                self.timeSinceMovement     = playTime

            self.currentPosition = self.trajectory[self.currentTrajectoryIdx]
        else:
            self.currentPosition = self.trajectory[self.trajectory.__len__() - 1]
            self.torpedoAtTarget = True

        sectorX = self.currentPosition.getX()
        sectorY = self.currentPosition.getY()

        super().update(sectorX, sectorY)

    def setTrajectory(self, trajectory: []):
        """"""
        self.trajectory = trajectory
