import logging
from random import random

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.engine.ShieldStatus import ShieldStatus
from org.hasii.pytrek.engine.PhaserStatus import PhaserStatus
from org.hasii.pytrek.engine.TorpedoStatus import TorpedoStatus
from org.hasii.pytrek.engine.ComputerStatus import ComputerStatus

from org.hasii.pytrek.GameStatistics import GameStatistics

from org.hasii.pytrek.gui.Enterprise import Enterprise

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Galaxy import Galaxy
from org.hasii.pytrek.objects.Quadrant import Quadrant

class GameEngine:
    """"""
    def __init__(self):
        """"""

        self.computer     = Computer()
        self.settings     = Settings()
        self.intelligence = Intelligence()
        self.logger       = logging.getLogger(__name__)
        self.stats        = GameStatistics()

        self.stats.skill        = self.settings.skill
        self.stats.gameType     = self.settings.gameType
        self.stats.energy       = self.settings.initialEnergyLevel
        self.stats.shieldEnergy = self.settings.initialShieldEnergy

        self.stats.shieldStatus   = ShieldStatus.Up
        self.stats.torpedoStatus  = TorpedoStatus.Up
        self.stats.phaserStatus   = PhaserStatus.Up
        self.stats.computerStatus = ComputerStatus.Up

        self.stats.starDate            = self.intelligence.getInitialStarDate()
        self.stats.remainingGameTime   = self.intelligence.getInitialGameTime()
        self.stats.remainingKlingons   = self.intelligence.getInitialKlingonCount(self.stats.remainingGameTime)
        self.stats.remainingCommanders = self.intelligence.getInitialCommanderCount()

    def impulse(self, newCoordinates: Coordinates, quadrant: Quadrant, enterprise: Enterprise):
        """"""

        travelDistance   = self.computer.computeQuadrantDistance(self.stats.currentSectorCoordinates, newCoordinates)
        quadrant.placeEnterprise(enterprise, newCoordinates)

        self.stats.currentSectorCoordinates = newCoordinates

        self.updateTimeAfterImpulseTravel(travelDistance=travelDistance)

        if self.stats.energy < self.settings.minimumImpulseEnergy:
            neededEnergyForImpulseMove = self.energy
        else:
            neededEnergyForImpulseMove = self.computeEnergyForQuadrantTravel(travelDistance=travelDistance)

        self.stats.energy = self.stats.energy - neededEnergyForImpulseMove

    def warp(self, moveToCoordinates: Coordinates, galaxy: Galaxy, intelligence: Intelligence, enterprise: Enterprise) -> Quadrant:
        """"""

        self.logger.info("Move to Quadrant: %s", moveToCoordinates)

        currentCoordinates: Coordinates = galaxy.currentQuadrant.coordinates
        distance:           float       = self.computer.computeGalacticDistance(startQuadrantCoordinates=currentCoordinates, endQuadrantCoordinates=moveToCoordinates)
        energyForWarp:      float       = self.computeEnergyForWarpTravel(travelDistance=distance, warpFactor=self.settings.warpFactor)
        #
        # Make sure starship has enough energy for the trip
        #
        if energyForWarp > self.stats.energy:
            return galaxy.currentQuadrant
        else:
            self.stats.energy = self.stats.energy - energyForWarp

        self.updateTimeAfterWarpTravel(travelDistance=distance, warpFactor=self.settings.warpFactor)
        quadrant: Quadrant     = galaxy.getQuadrant(moveToCoordinates)
        galaxy.currentQuadrant = quadrant

        sectorCoordinates: Coordinates = intelligence.getRandomSectorCoordinates()

        quadrant.placeEnterprise(enterprise, sectorCoordinates)

        self.stats.currentSectorCoordinates   = sectorCoordinates
        self.stats.currentQuadrantCoordinates = moveToCoordinates

        return quadrant

    def updateTimeAfterImpulseTravel(self, travelDistance: float ):
        """

        Time = dist/0.095;

        :param travelDistance:
        :return:
        """
        elapsedTime = travelDistance / 0.095
        self.updateTime(elapsedTime=elapsedTime)

    def updateTimeAfterWarpTravel(self, travelDistance: float, warpFactor: float):
        """
        Time = 10.0*dist/wfacsq;
        :return:
        """
        wfacsq:      float = warpFactor ** 2
        elapsedTime: float = 10.0 * travelDistance / wfacsq

        self.updateTime(elapsedTime=elapsedTime)

    def updateTime(self, elapsedTime: float):
        """"""

        # oldTime      = self.stats.remainingGameTime
        # oldStarDate  = self.stats.starDate

        self.stats.starDate          = self.stats.starDate + elapsedTime;
        self.stats.remainingGameTime = self.stats.remainingGameTime - elapsedTime

    def computeEnergyForQuadrantTravel(self, travelDistance: float) -> float:
        """
          power = 20.0 + 100.0*dist;

        :param travelDistance: How far
        :return:  The energy necessary to do inter-quadrant travel
        """

        quadrantEnergy: float = 20 + (100.0 * travelDistance);

        self.logger.debug("theTravelDistance: '%s' quadrantEnergy : '%s'", travelDistance, quadrantEnergy)

        return quadrantEnergy

    def computeEnergyForWarpTravel(self, travelDistance: float, warpFactor: float) -> float:
        """

        :param travelDistance: How far
        :param warpFactor:     How fast

        :return:  The energy need to travel this far.
        """
        wCube:          float = warpFactor ** 3
        shieldValue:    int   = self.stats.shieldStatus.value
        requiredEnergy: float = (travelDistance + 0.05) + wCube * (shieldValue + 1)

        return requiredEnergy