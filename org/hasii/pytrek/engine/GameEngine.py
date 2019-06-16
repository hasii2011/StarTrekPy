

import logging

from math import atan2
from math import fabs
from math import sqrt
from math import sin

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.engine.ShieldStatus import ShieldStatus
from org.hasii.pytrek.engine.PhaserStatus import PhaserStatus
from org.hasii.pytrek.engine.TorpedoStatus import TorpedoStatus
from org.hasii.pytrek.engine.ComputerStatus import ComputerStatus
from org.hasii.pytrek.engine.ShieldHitData import ShieldHitData

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
            neededEnergyForImpulseMove = self.stats.energy
        else:
            neededEnergyForImpulseMove = self.computeEnergyForQuadrantTravel(travelDistance=travelDistance)

        self.stats.energy = self.stats.energy - neededEnergyForImpulseMove

    def warp(self, moveToCoordinates: Coordinates, galaxy: Galaxy, intelligence: Intelligence, enterprise: Enterprise) -> Quadrant:
        """"""

        self.logger.info("Move to Quadrant: %s", moveToCoordinates)

        currentCoordinates: Coordinates = galaxy.currentQuadrant.coordinates
        distance:           float       = self.computer.computeGalacticDistance(startQuadrantCoordinates=currentCoordinates,
                                                                                endQuadrantCoordinates=moveToCoordinates)
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

    def updateTimeAfterImpulseTravel(self, travelDistance: float):
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

        self.stats.starDate          = self.stats.starDate + elapsedTime
        self.stats.remainingGameTime = self.stats.remainingGameTime - elapsedTime

    def computeEnergyForQuadrantTravel(self, travelDistance: float) -> float:
        """
          power = 20.0 + 100.0*dist;

        :param travelDistance: How far
        :return:  The energy necessary to do inter-quadrant travel
        """

        quadrantEnergy: float = 20 + (100.0 * travelDistance)

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

    def degradeShields(self, shieldAbsorptionValue: float):

        if shieldAbsorptionValue > self.stats.shieldEnergy:
            shieldAbsorptionValue = self.stats.shieldEnergy
        self.stats.shieldEnergy -= shieldAbsorptionValue

    def degradeEnergyLevel(self, degradedTorpedoValue: float):
        """
        printf("Hit %g energy %g\n", hit, energy);
        energy -= hit;

        Args:
            degradedTorpedoValue: Value of torpedo hit after accounting for
            the hit on the shield
        """
        self.stats.energy -= degradedTorpedoValue
        self.logger.info(f"{self.stats.energy:.4f}")

    def computeShieldHit(self, torpedoHit: float) -> ShieldHitData:
        """

        pfac = 1.0/inshld;

        # shields will take hits
        double absorb, hitsh, propor = pfac*shield;

        if(propor < 0.1)
            propor = 0.1;
        hitsh = propor*chgfac*hit+1.0;
        atackd=1;
        absorb = 0.8*hitsh;
        if (absorb > shield)
            absorb = shield;
        shield -= absorb;
        hit -= hitsh;

        Returns: Computed shield hit data
        """
        changeFactor = 0.25 + (0.5 * self.intelligence.rand())
        proportionalFactor = 1.0 / Settings.DEFAULT_FULL_SHIELDS
        proportion = proportionalFactor * self.stats.shieldEnergy

        if proportion < 0.1:
            proportion = 0.1
        shieldHit = proportion * changeFactor * torpedoHit + 1.0

        shieldAbsorptionValue: float = 0.8 * shieldHit
        # if shieldAbsorptionValue > self.stats.shieldEnergy:
        #     shieldAbsorptionValue = self.stats.shieldEnergy
        # self.stats.shieldEnergy -= shieldAbsorptionValue

        torpedoHit -= shieldHit

        shieldHitData: ShieldHitData = ShieldHitData()

        shieldHitData.shieldAbsorptionValue   = shieldAbsorptionValue
        shieldHitData.degradedTorpedoHitValue = torpedoHit

        return shieldHitData

    def computeHit(self, shooterPosition: Coordinates, targetPosition: Coordinates, klingonPower: float) -> float:
        """
         StarTrekScreen: Yowzah!  A dirty rotten Klingon at (7,7) took a shot at me (3,7)

        jx,jy is section position of shooter
        sectx,secty is section position of what we hit

        r = (Rand()+Rand())*0.5 -0.5;
        r += 0.002*kpower[l]*r;

        double course = 1.90985 * atan2((double)secty-jy, (double)jx-sectx);
        double ac = course + 0.25*r;
        double angle = (15.0-ac)*0.5235988;
        double bullseye = (15.0 - course)*0.5235988;

        inx,iny is sector position of thing we hit

        *hit = 700.0 + 100.0*Rand() - 1000.0*sqrt(square(ix-inx)+square(iy-iny)) * fabs(sin(bullseye-angle));
        *hit = fabs(*hit);

        Returns:

        """
        r: float = (self.intelligence.rand() + self.intelligence.rand()) * 0.5 - 0.5

        r += 0.002 * klingonPower * r
        self.logger.debug(f"r: {r}")

        jx = shooterPosition.getX()
        jy = shooterPosition.getY()

        sectx = targetPosition.getX()
        secty = targetPosition.getY()

        rads = atan2(secty-jy, jx-sectx)
        self.logger.debug(f" (jx,jy): ({jx}, {jy}), (sectx,secty): ({sectx},{secty}) - rads: {rads}")

        course: float = (1.90985 * rads) + (0.25 * r)
        self.logger.debug(f"course: {course}")

        ac: float = course + 0.25 * r

        angle:    float = (15.0-ac) * 0.5235988
        bullseye: float = (15.0 - course)*0.5235988

        self.logger.debug(f"angle: {angle}  bullseye {bullseye}")

        inx = targetPosition.getX()
        iny = targetPosition.getY()
        ix  = shooterPosition.getX()
        iy  = shooterPosition.getY()

        def square(num) -> float:
            return num * num

        hit = 700.0 + (100.0 * self.intelligence.rand()) - \
            (1000.0 * sqrt(square(ix-inx) + square(iy-iny))) * fabs(sin(bullseye-angle))

        return hit
