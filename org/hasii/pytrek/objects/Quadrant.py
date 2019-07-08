
from typing import List
from typing import cast

from logging import getLogger
from logging import Logger

import pygame

from pygame import Surface
from pygame.sprite import Sprite
from pygame.event import Event
from pygame.event import post as pygamePostEvent

from org.hasii.pytrek.engine.Intelligence import Intelligence

from org.hasii.pytrek.gui.gamepieces.Enterprise import Enterprise
from org.hasii.pytrek.gui.gamepieces.Explosion import Explosion
from org.hasii.pytrek.gui.gamepieces.StarBase import StarBase
from org.hasii.pytrek.gui.gamepieces.Klingon import Klingon
from org.hasii.pytrek.gui.gamepieces.Commander import Commander
from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece
from org.hasii.pytrek.gui.gamepieces.BasicMiss import BasicMiss
from org.hasii.pytrek.gui.gamepieces.BigRedX import BigRedX
from org.hasii.pytrek.gui.gamepieces.BasicTorpedo import BasicTorpedo
from org.hasii.pytrek.gui.gamepieces.PhotonTorpedo import PhotonTorpedo
from org.hasii.pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo
from org.hasii.pytrek.gui.gamepieces.KlingonTorpedoMiss import KlingonTorpedoMiss

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Sector import Sector
from org.hasii.pytrek.objects.SectorType import SectorType

from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.GameStatistics import GameStatistics


class Quadrant:
    """
    Quadrant Management
    """
    def __init__(self, coordinates: Coordinates, screen: Surface):
        """
            Initialize a quadrant
        """

        self.coordinates: Coordinates = coordinates
        self.screen:      Surface     = screen
        self.logger:      Logger      = getLogger(__name__)

        self.stats:        GameStatistics = GameStatistics()
        self.settings:     Settings       = Settings()
        self.intelligence: Intelligence   = Intelligence()

        self._klingonCount:   int  = 0
        self._commanderCount: int = 0

        self.klingons:   List[Klingon]   = []
        self.commanders: List[Commander] = []
        self.starBase:       bool        = False
        self.starBaseCoords: Coordinates = cast(Coordinates, None)

        self.enterprise:            Enterprise  = cast(Enterprise, None)
        self.enterpriseCoordinates: Coordinates = cast(Coordinates, None)

        self.sectors: List[Sector] = []

        for i in range(Intelligence.QUADRANT_HEIGHT):
            row: List[Sector] = []
            for j in range(Intelligence.QUADRANT_WIDTH):

                sector = Sector(cast(Sprite, None), SectorType.EMPTY, i, j)
                row.append(sector)
                self.logger.debug("Created empty sector (%s,%s)", str(i), str(j))
            self.sectors.append(row)

    def update(self, playTime: float):
        """"""
        sectorX = 0
        for sectorRow in self.sectors:

            sectorY = 0
            for sector in sectorRow:
                gamePiece  = sector.sprite
                sectorType = sector.getType()

                if sectorType != SectorType.EMPTY:

                    self.logger.debug(f"Update sectorType: {sectorType}")
                    if sectorType == SectorType.PHOTON_TORPEDO:

                        photonTorpedo: PhotonTorpedo = cast(PhotonTorpedo, gamePiece)
                        photonTorpedo.update(sectorX, sectorY, playTime)

                        ptPosition = photonTorpedo.currentPosition
                        currentSectorCoordinates = Coordinates(sectorX, sectorY)

                        if not currentSectorCoordinates.__eq__(ptPosition):
                            self.makeSectorAtCoordinatesEmpty(currentSectorCoordinates)
                            self.placeSprite(photonTorpedo, SectorType.PHOTON_TORPEDO, ptPosition)
                        self.attemptKlingonKill(photonTorpedo, playTime, sector)
                    elif sectorType == SectorType.KLINGON_TORPEDO:

                        klingonTorpedo: KlingonTorpedo = cast(KlingonTorpedo, gamePiece)
                        klingonTorpedo.update(sectorX, sectorY, playTime)

                        ktNextPosition = klingonTorpedo.currentPosition
                        currentSectorCoordinates = Coordinates(sectorX, sectorY)
                        if not currentSectorCoordinates.__eq__(ktNextPosition):
                            self.makeSectorAtCoordinatesEmpty(currentSectorCoordinates)
                            self.placeSprite(klingonTorpedo, SectorType.KLINGON_TORPEDO, ktNextPosition)

                        enterpriseHit: bool = self.checkIfEnterpriseHit(klingonTorpedo, playTime)
                        if enterpriseHit is True:
                            self._tellGameLoop(klingonTorpedo)
                            self.placeEnterprise(enterprise=self.enterprise, coordinates=ktNextPosition)

                    elif sectorType == SectorType.EXPLOSION:

                        explosion: Explosion = cast(Explosion, gamePiece)
                        if explosion.lastExplosion is True:
                            self.makeSectorAtCoordinatesEmpty(explosion.currentPosition)
                        else:
                            explosion.update(sectorX, sectorY, playTime)
                    elif sectorType == SectorType.COMMANDER:
                        commander: Commander = cast(Commander, gamePiece)
                        changedSectorCoordinates = commander.update(sectorX, sectorY, playTime)
                        currentSectorCoordinates = Coordinates(sectorX, sectorY)
                        if not changedSectorCoordinates.__eq__(currentSectorCoordinates):
                            while True:
                                if self.isSectorEmpty(changedSectorCoordinates) is True:
                                    break
                                else:
                                    changedSectorCoordinates = commander.evade(currentSectorCoordinates)

                            self.logger.debug("Commander moved from '%s' to '%s", currentSectorCoordinates, changedSectorCoordinates)
                            self.moveCommander(commander, currentSectorCoordinates, changedSectorCoordinates)
                    elif sectorType == SectorType.KLINGON or sectorType == SectorType.KLINGON_TORPEDO_MISS:
                        klingon: Klingon = cast(Klingon, gamePiece)
                        klingon.update(sectorX, sectorY, playTime)
                    elif sectorType == sectorType.BIG_RED_X:

                        basicMiss: BasicMiss = cast(BasicMiss, gamePiece)
                        basicMiss.update(sectorX, sectorY, playTime)
                        if basicMiss.eligibleToRemove is True:
                            self.logger.debug("Current sector sectorX: '%s', sectorY: '%s", sectorX, sectorY)
                            self.makeSectorAtCoordinatesEmpty(basicMiss.currentPosition)
                    else:
                        gamePiece.update(sectorX, sectorY, playTime)
                sectorY += 1
            sectorX += 1

    def attemptKlingonKill(self, torpedo: BasicTorpedo, playTime: float, sector: Sector):
        """
            Did I hit a Klingon

        Args:
            torpedo: The torpedo to check
            playTime: The current game time
            sector: The sector we are in

        Returns:
        """
        klingonGroup = pygame.sprite.Group()

        for klingon in self.klingons:
            klingonGroup.add(klingon)
        for commander in self.commanders:
            klingonGroup.add(commander)
        killedKlingons: list = pygame.sprite.spritecollide(torpedo, klingonGroup, False)
        #
        self.logger.debug(f"Killed klingon count: {len(killedKlingons)}")
        #
        if killedKlingons.__len__() > 0:
            for deadKlingon in killedKlingons:
                self.logger.debug(f"deadKlingon at: {deadKlingon.currentPosition}")
                sector.sectorType = SectorType.EMPTY
                sector.sprite = None

                if isinstance(deadKlingon, Klingon):
                    self.removeKlingon(deadKlingon)
                    self.placeAnExplosion(deadKlingon.currentPosition, playTime)
                else:
                    self.removeCommander(deadKlingon)
                    self.placeAnExplosion(deadKlingon.currentPosition, playTime)
        else:
            self.logger.debug(f"torpedoAtTarget: {torpedo.torpedoAtTarget}")
            if torpedo.torpedoAtTarget is True:
                self.logger.info(f"ARRGGHH!! we missed.  Torpedo coordinate: '{torpedo.currentPosition}'")
                self.makeSectorAtCoordinatesEmpty(coordinates=torpedo.currentPosition)
                bigRedX = BigRedX(screen=self.screen, playTime=playTime)
                bigRedX.currentPosition = torpedo.currentPosition
                self.placeSprite(sprite=bigRedX, sectorType=SectorType.BIG_RED_X, coordinates=torpedo.currentPosition)

    def checkIfEnterpriseHit(self, torpedo: KlingonTorpedo, playTime: float) -> bool:
        """

        Args:
            torpedo: The torpedo that may hit the Enterprise
            playTime: The current game playtime

        Returns:

        """
        thereWasAHit: bool = False

        enterpriseGroup = pygame.sprite.Group()
        enterpriseGroup.add(self.enterprise)
        enterpriseHit: list = pygame.sprite.spritecollide(torpedo, enterpriseGroup, False)
        if enterpriseHit.__len__() > 0:
            thereWasAHit = True
        else:
            if torpedo.torpedoAtTarget is True:
                self.logger.info(f"Ha ha Klingon missed.  Torpedo coordinate: '{torpedo.currentPosition}'")
                self.makeSectorAtCoordinatesEmpty(coordinates=torpedo.currentPosition)
                torpedoMiss: KlingonTorpedoMiss = KlingonTorpedoMiss(screen=self.screen, playTime=playTime)
                torpedoMiss.currentPosition = torpedo.currentPosition
                self.placeSprite(sprite=torpedoMiss,
                                 sectorType=SectorType.KLINGON_TORPEDO_MISS, coordinates=torpedoMiss.currentPosition)

        self.logger.debug(f"Did Klingon torpedo hit Enterprise: '{thereWasAHit}'")
        return thereWasAHit

    def addKlingon(self):
        """"""
        self._klingonCount += 1
        klingon = self.placeAKlingon()
        self.klingons.append(klingon)

    def removeKlingon(self, deadKlingon: Klingon):
        """
        No need to actually remove the sprite that is the Klingon;  When
        we place the explosion it will be replaced

        Args:
            deadKlingon:
        """
        self.klingons.remove(deadKlingon)
        self._klingonCount -= 1
        self.stats.remainingKlingons -= 1

    def getKlingons(self) -> List[Klingon]:
        """
        Returns: a list of Klingons in the current quadrant
        """
        return self.klingons

    def removeCommander(self, deadCommander: Commander):
        """"""
        self.commanders.remove(deadCommander)
        self._commanderCount -= 1
        self.stats.remainingCommanders -= 1

    def getKlingonCount(self):
        """"""
        return self._klingonCount

    def getCommanderCount(self):
        return self._commanderCount

    def getSuperCommanderCount(self):
        return 0

    def getRomulanCount(self):
        return 0

    def addStarBase(self):
        """"""
        self.starBase = True
        self.placeAStarBase()

    def hasStarBase(self):
        """"""
        return self.starBase

    def addCommander(self):
        """"""
        self._commanderCount += 1
        commander = self.placeACommander()
        self.commanders.append(commander)

    def getCommanderCount(self):
        """"""
        return self.commanders

    def getCoordinates(self) -> Coordinates:
        """"""
        return self.coordinates

    def getSector(self, sectorCoordinates: Coordinates) -> Sector:
        """"""
        sectorRow = self.sectors.__getitem__(sectorCoordinates.getX())

        sector = sectorRow.__getitem__(sectorCoordinates.getY())

        return sector

    def placeEnterprise(self, enterprise: Enterprise, coordinates: Coordinates):
        """

        Args:
            enterprise:     The fighting ship to place in this quadrant

            coordinates:    The sector coordinates in which to place the Enterprise
        """
        if self.enterpriseCoordinates is not None:

            oldEnterpriseRow = self.sectors.__getitem__(self.enterpriseCoordinates.getX())
            oldSector        = oldEnterpriseRow.__getitem__(self.enterpriseCoordinates.getY())
            oldSector.setType(SectorType.EMPTY)
            oldSector.sprite = None

        self.logger.debug(f"Placing enterprise @quadrant: {coordinates}")

        sectorRow = self.sectors.__getitem__(coordinates.getX())
        sector    = sectorRow.__getitem__(coordinates.getY())

        sector.setType(SectorType.ENTERPRISE)
        sector.setCoordinates(coordinates)
        self.logger.info(f"Enterprise @sector: {coordinates}")

        sector.setSprite(enterprise)
        self.enterprise = enterprise
        enterprise.currentPosition = coordinates
        self.enterpriseCoordinates = coordinates

    def placeAStarBase(self):
        """Randomly place a starbase"""

        self.logger.debug(f"Starbase @Quadrant {self.coordinates}")

        sector: Sector     = self.getRandomEmptySector()
        sector.sectorType  = SectorType.STARBASE
        starBase: StarBase = StarBase(screen=self.screen)

        sector.setSprite(starBase)
        self.starBaseCoords = sector.getCoordinates()

        self.logger.debug(f"Star Base @Sector {sector}")

    def placeAnExplosion(self, coordinates: Coordinates, playTime: float):
        """"""
        explosion = Explosion(screen=self.screen)
        self.logger.debug(f"Placing an explosion at: {coordinates}")

        explosion.currentPosition        = coordinates
        explosion.timeSinceLastExplosion = playTime

        self.placeSprite(explosion, SectorType.EXPLOSION, coordinates)

    def placeAKlingon(self) -> Klingon:
        """

        """
        sector            = self.getRandomEmptySector()
        sector.sectorType = SectorType.KLINGON
        klingon           = Klingon(screen=self.screen, coordinates=sector.getCoordinates())
        kpower            = self.intelligence.computeKlingonPower()

        klingon.setPower(kpower)
        sector.setSprite(klingon)

        self.logger.debug(f"Placed klingon at: quadrant: {self.coordinates}  sector: {sector}, power {kpower}")
        return klingon

    def placeACommander(self) -> Commander:
        """"""
        sector            = self.getRandomEmptySector()
        sector.sectorType = SectorType.COMMANDER
        commander         = Commander(screen=self.screen, coordinates=sector.getCoordinates())
        cPower            = self.intelligence.computeCommanderPower()

        commander.setPower(cPower)
        sector.setSprite(commander)

        self.logger.debug(f"Placed commander at: quadrant: {self.coordinates}  sector: {sector}  power {cPower}")
        return commander

    def placeATorpedo(self, coordinates: Coordinates, torpedo: BasicTorpedo, torpedoType: SectorType):
        """"""

        torpedoSector = self.getSector(sectorCoordinates=coordinates)

        torpedoSector.sectorType = torpedoType
        torpedoSector.setSprite(torpedo)
        self.logger.debug(f"Torpedo position {coordinates}")

    def getRandomEmptySector(self) -> Sector:
        """"""

        randomSectorCoordinates = self.intelligence.getRandomSectorCoordinates()
        sector                  = self.getSector(randomSectorCoordinates)

        while sector.getType() != SectorType.EMPTY:
            randomSectorCoordinates = self.intelligence.getRandomSectorCoordinates()
            sector = self.getSector(randomSectorCoordinates)

        return sector

    def moveCommander(self, commander: Commander, oldSectorCoordinates: Coordinates, newSectorCoordinates: Coordinates):
        """"""
        self.makeSectorAtCoordinatesEmpty(oldSectorCoordinates)
        self.placeSprite(commander, SectorType.COMMANDER, newSectorCoordinates)

    def makeSectorAtCoordinatesEmpty(self, coordinates: Coordinates):
        """"""
        rowIdx    = coordinates.getX()
        columnIdx = coordinates.getY()
        sectorRow = self.sectors[rowIdx]

        oldSector: Sector    = sectorRow[columnIdx]
        oldSector.sectorType = SectorType.EMPTY
        oldSector.sprite     = None

        sectorRow[columnIdx] = oldSector

    def placeSprite(self, sprite: GamePiece, sectorType: SectorType, coordinates: Coordinates):
        """"""
        rowIdx    = coordinates.getX()
        columnIdx = coordinates.getY()
        sectorRow = self.sectors[rowIdx]

        spriteSector: Sector    = sectorRow[columnIdx]
        spriteSector.sectorType = sectorType
        spriteSector.sprite     = sprite

        sectorRow[columnIdx]    = spriteSector

    def isSectorEmpty(self, coordinates: Coordinates) -> bool:
        """"""
        ans:           bool   = False
        sectorToCheck: Sector = self.getSectorByCoordinates(coordinates)

        if sectorToCheck.sectorType == SectorType.EMPTY:
            ans = True

        return ans

    def getSectorByCoordinates(self, coordinates: Coordinates) -> Sector:
        """"""
        rowIdx    = coordinates.getX()
        columnIdx = coordinates.getY()
        sectorRow = self.sectors[rowIdx]

        sector: Sector = sectorRow[columnIdx]
        return sector

    def _tellGameLoop(self, torpedo: KlingonTorpedo):

        self.logger.info(f"Tell game loop that the Enterprise was hit!")

        enterpriseHitEvent = Event(Settings.ENTERPRISE_HIT_BY_TORPEDO_EVENT, dict=None)
        enterpriseHitEvent.dict['enterprisePosition'] = self.enterprise.currentPosition
        enterpriseHitEvent.dict['shooterPosition'] = torpedo.shooterPosition
        enterpriseHitEvent.dict['shooterPower'] = torpedo.shooterPower

        pygamePostEvent(enterpriseHitEvent)

    def debugSectors(self):

        self.logger.debug("************************* Start Quadrant Dump *****************************")
        for sectorRow in self.sectors:
            for sector in sectorRow:
                self.logger.debug(f"sector: ({str(sector.sectorX)},{str(sector.sectorY)}) type: {sector.sectorType.name}")
        self.logger.debug("************************* End Quadrant Dump *****************************")
