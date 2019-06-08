import logging

import pygame

from pygame import Surface

from org.hasii.pytrek.engine.Intelligence import Intelligence

from org.hasii.pytrek.gui import Enterprise
from org.hasii.pytrek.gui.Explosion import Explosion
from org.hasii.pytrek.gui.StarBase import StarBase
from org.hasii.pytrek.gui.Klingon import Klingon
from org.hasii.pytrek.gui.Commander import Commander
from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.gui.BigRedX import BigRedX

from org.hasii.pytrek.gui.BasicTorpedo import BasicTorpedo

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Sector import Sector
from org.hasii.pytrek.objects.SectorType import SectorType

from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.GameStatistics import GameStatistics

class Quadrant():
    """Quadrant Management"""
    def __init__(self, coordinates: Coordinates, screen: Surface):
        """
            Initialize a quadrant
        """

        self.coordinates = coordinates
        self.screen      = screen

        self.stats        = GameStatistics()
        self.intelligence = Intelligence()
        self.settings     = Settings()

        self.klingonCount   = 0
        self.commandCount   = 0
        self.commanderCount = 0

        self.klingons   = []
        self.commanders = []
        self.starBase   = False

        self.enterpriseCoordinates = None

        self.logger = logging.getLogger(__name__)

        self.sectors = []
        for i in range(Intelligence.QUADRANT_HEIGHT):
            row =[]
            for j in range(Intelligence.QUADRANT_WIDTH):

                sector = Sector(None, SectorType.EMPTY, i,j)
                row.append(sector)
                self.logger.debug("Created empty sector (%s,%s)", str(i), str(j))
            self.sectors.append(row)

    def placeEnterprise(self, enterprise: Enterprise, coordinates: Coordinates):
        """

        :param enterprise:   The fighting ship to place in this quadrant
        :param coordinates:  The sector coordinates in which to place the Enterprise

        :return:
        """
        if self.enterpriseCoordinates != None:

            oldEnterpriseRow = self.sectors.__getitem__(self.enterpriseCoordinates.getX())
            oldSector        = oldEnterpriseRow.__getitem__(self.enterpriseCoordinates.getY())
            oldSector.setType(SectorType.EMPTY)
            oldSector.sprite = None

        self.logger.debug("Placing enterprise at: %s",coordinates.__str__())

        sectorRow = self.sectors.__getitem__(coordinates.getX())
        sector    = sectorRow.__getitem__(coordinates.getY())

        sector.setType(SectorType.ENTERPRISE)
        sector.setCoordinates(coordinates)
        self.logger.info("Enterprise @sector: %s", coordinates)

        sector.setSprite(enterprise)
        enterprise.currentPosition = coordinates
        self.enterpriseCoordinates = coordinates

    def placeAStarBase(self):
        """Randomly place a starbase"""

        self.logger.debug("Starbase @Quadrant %s", self.coordinates)

        sector            = self.getRandomEmptySector()
        sector.sectorType = SectorType.STARBASE
        starBase          = StarBase(screen=self.screen)
        sector.setSprite(starBase)
        self.logger.debug("Star Base set at sector (%s,%s)", sector.sectorX, sector.sectorY)

    def placeATorpedo(self, coordinates: Coordinates, torpedo: BasicTorpedo):
        """"""

        torpedoSector = self.getSector(sectorCoordinates=coordinates)

        torpedoSector.sectorType = SectorType.PHOTON_TORPEDO
        torpedoSector.setSprite(torpedo)
        self.logger.debug("Torpedo position %s", coordinates)

    def update(self, playTime: float):
        """"""
        sectorX = 0
        for sectorRow in self.sectors:

            sectorY = 0
            for sector in sectorRow:
                gamePiece  = sector.sprite
                sectorType = sector.getType()

                if sectorType != SectorType.EMPTY:

                    self.logger.debug("Update sectorType: %s", sectorType)
                    if sectorType == SectorType.PHOTON_TORPEDO:

                        gamePiece.update(sectorX, sectorY, playTime)
                        gamePiecePosition = gamePiece.currentPosition
                        currentSectorCoordinates = Coordinates(sectorX, sectorY)
                        if not currentSectorCoordinates.__eq__(gamePiecePosition):
                            self.makeSectorAtCoordinatesEmpty(currentSectorCoordinates)
                            self.placeSprite(gamePiece, SectorType.PHOTON_TORPEDO, gamePiecePosition)
                        self.attemptKlingonKill(gamePiece, playTime, sector)
                    elif sectorType == SectorType.EXPLOSION:

                        explosion: Explosion = gamePiece
                        if explosion.lastExplosion == True:
                            self.makeSectorAtCoordinatesEmpty(explosion.currentPosition)
                        else:
                            explosion.update(sectorX, sectorY, playTime)
                    elif sectorType == SectorType.COMMANDER:
                        commander: Commander = gamePiece
                        changedSectorCoordinates = commander.update(sectorX, sectorY, playTime)
                        currentSectorCoordinates = Coordinates(sectorX, sectorY)
                        if not changedSectorCoordinates.__eq__(currentSectorCoordinates):
                            while True:
                                if self.isSectorEmpty(changedSectorCoordinates) == True:
                                    break
                                else:
                                    changedSectorCoordinates = commander.evade(currentSectorCoordinates)

                            self.logger.debug("Commander moved from '%s' to '%s", currentSectorCoordinates, changedSectorCoordinates)
                            self.moveCommander(commander, currentSectorCoordinates, changedSectorCoordinates)
                    elif sectorType == SectorType.KLINGON:
                        klingon: Klingon = gamePiece
                        klingon.update(sectorX, sectorY, playTime)
                        if klingon.timeToShoot == True:
                            self.logger.info("IT IS TIME TO SHOOT BACK")
                    elif sectorType == sectorType.BIG_RED_X:

                        bigRedX: BigRedX = gamePiece
                        bigRedX.update(sectorX, sectorY, playTime)
                        if bigRedX.eligibleToRemove == True:
                            self.logger.debug("Current sector sectorX: '%s', sectorY: '%s", sectorX, sectorY)
                            self.makeSectorAtCoordinatesEmpty(bigRedX.currentPosition)

                    else:
                        gamePiece.update(sectorX, sectorY, playTime)
                sectorY +=1
            sectorX +=1

    def attemptKlingonKill(self, torpedo: BasicTorpedo, playTime, sector):
        """
            Did I hit a Klingon

        :param torpedo:
        :param playTime:
        :param sector:
        :return:
        """
        klingonGroup = pygame.sprite.Group()

        for klingon in self.klingons:
            klingonGroup.add(klingon)
        for commander in self.commanders:
            klingonGroup.add(commander)
        killedKlingons: list = pygame.sprite.spritecollide(torpedo, klingonGroup, False)
        #
        # Either we killed some or we missed
        #
        if killedKlingons.__len__() > 0:
            for deadKlingon in killedKlingons:
                self.logger.debug("deadKlingon at: %s", deadKlingon.currentPosition)
                sector.sectorType = SectorType.EMPTY
                sector.sprite = None


                if isinstance(deadKlingon, Klingon):
                    self.removeKlingon(deadKlingon)
                    self.placeAnExplosion(deadKlingon.currentPosition, playTime)
                else:
                    self.removeCommander(deadKlingon)
                    self.placeAnExplosion(deadKlingon.currentPosition, playTime)
        else:
            if torpedo.torpedoAtTarget == True:
                self.logger.debug("ARRGGHH!! we missed.  Torpedo coordinate: '%s", torpedo.currentPosition)
                self.makeSectorAtCoordinatesEmpty(coordinates=torpedo.currentPosition)
                bigRedX = BigRedX(screen=self.screen, playTime=playTime)
                bigRedX.currentPosition = torpedo.currentPosition
                self.placeSprite(sprite=bigRedX,sectorType=SectorType.BIG_RED_X, coordinates=torpedo.currentPosition)

    def addKlingon(self):
        """"""
        self.klingonCount +=1
        klingon = self.placeAKlingon()
        self.klingons.append(klingon)

    def removeKlingon(self, deadKlingon: Klingon):
        """
        No need to actually remove the sprite that is the Klingon;  When
        we place the explosion it will be replaced

        :param deadKlingon:
        :return:
        """
        self.klingons.remove(deadKlingon)
        self.klingonCount -= 1
        self.stats.remainingKlingons -= 1

    def removeCommander(self, deadCommander: Commander):
        """"""
        self.commanders.remove(deadCommander)
        self.commanderCount -= 1
        self.stats.remainingCommanders -= 1

    def getKlingonCount(self):
        """"""
        return self.klingonCount

    def addStarBase(self):
        """"""
        self.starBase = True
        self.placeAStarBase()

    def hasStarBase(self):
        """"""
        return self.starBase

    def addCommander(self):
        """"""
        self.commanderCount += 1
        commander = self.placeACommander()
        self.commanders.append(commander)

    def getCommandCount(self):
        """"""
        return self.commanders

    def getCoordinates(self)->Coordinates:
        """"""
        return self.coordinates

    def getSector(self, sectorCoordinates: Coordinates)->Sector:
        """"""
        sectorRow = self.sectors.__getitem__(sectorCoordinates.getX())

        sector = sectorRow.__getitem__(sectorCoordinates.getY())

        return sector

    def placeAnExplosion(self, coordinates: Coordinates, playTime: float):
        """"""
        explosion = Explosion(screen=self.screen)
        self.logger.debug("Placing an explosion at: %s", coordinates)

        explosion.currentPosition        = coordinates
        explosion.timeSinceLastExplosion = playTime

        self.placeSprite(explosion, SectorType.EXPLOSION, coordinates)

    def placeAKlingon(self) -> Klingon:
        """"""
        sector            = self.getRandomEmptySector()
        sector.sectorType = SectorType.KLINGON
        klingon           = Klingon(screen=self.screen, coordinates=sector.getCoordinates())
        sector.setSprite(klingon)

        self.logger.debug("Placed klingon at: quadrant: %s  sector: %s", self.coordinates, sector)
        return klingon

    def placeACommander(self) -> Commander:
        """"""
        sector            = self.getRandomEmptySector()
        sector.sectorType = SectorType.COMMANDER
        commander         = Commander(screen=self.screen, coordinates=sector.getCoordinates())
        sector.setSprite(commander)

        self.logger.debug("Placed commander at: quadrant: %s  sector: %s", self.coordinates, sector)
        return commander

    def getRandomEmptySector(self)->Sector:
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

    def isSectorEmpty(self, coordinates: Coordinates)->bool:
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

    def debugSectors(self):

        self.logger.debug("************************* Start Quadrant Dump *****************************")
        for sectorRow in self.sectors:
            for sector in sectorRow:
                self.logger.debug("sector: (" + str(sector.sectorX) +
                                ","                +
                                    str(sector.sectorY) +
                               ") type: " + sector.sectorType.name)
        self.logger.debug("************************* End Quadrant Dump *****************************")
