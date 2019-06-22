
import sys

import os

import logging

from typing import List

import pygame

from pygame import Surface
from pygame.event import Event

from albow.core.ui.Screen import Screen
from albow.core.ui.Shell import Shell
from albow.core.ui.RootWidget import RootWidget
from albow.core.UserEventCall import UserEventCall

from albow.dialog.DialogUtilities import ask

from org.hasii.pytrek.GameStatistics import GameStatistics
from org.hasii.pytrek.GameMode import GameMode
from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Galaxy import Galaxy
from org.hasii.pytrek.objects.Quadrant import Quadrant
from org.hasii.pytrek.objects.SectorType import SectorType

from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.engine.Direction import Direction
from org.hasii.pytrek.engine.ShieldHitData import ShieldHitData

from hasii.pytrek.gui.gamepieces.Enterprise import Enterprise
from org.hasii.pytrek.gui.GalaxyScanBackground import GalaxyScanBackground
from org.hasii.pytrek.gui.MessageConsole import MessageConsole

from org.hasii.pytrek.gui.QuadrantBackground import QuadrantBackground
from org.hasii.pytrek.gui.status.StatusConsole import StatusConsole
from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.gui.Klingon import Klingon
from org.hasii.pytrek.gui.PhotonTorpedo import PhotonTorpedo
from org.hasii.pytrek.gui.KlingonTorpedo import KlingonTorpedo


class StarTrekScreen(Screen):

    MAX_X_POS = Intelligence.GALAXY_WIDTH * GamePiece.QUADRANT_PIXEL_WIDTH

    _myself: 'StarTrekScreen' = None

    def __init__(self, shell: Shell, theSurface: Surface):

        super().__init__(shell)

        self.logger = logging.getLogger(__name__)
        #
        # Debug logger
        #
        # saveLogger = self.logger
        # while self.logger is not None:
        #     print(f"level: '{self.logger.level}'', name: '{self.logger.name}'', handlers: '{self.logger.handlers}"'')
        #     self.logger = self.logger.parent
        # self.logger = saveLogger

        self.surface = theSurface

        self.settings = Settings()
        self.computer = Computer()

        self.statistics = GameStatistics()
        self.intelligence = Intelligence()

        self.soundUnableToComply = pygame.mixer.Sound(os.path.join('sounds', 'tos_unabletocomply.wav'))
        self.soundInaccurate     = pygame.mixer.Sound(os.path.join('sounds', 'tos_inaccurateerror_ep.wav'))
        self.soundWarp           = pygame.mixer.Sound(os.path.join('sounds', 'tos_flyby_1.wav'))
        self.soundImpulse        = pygame.mixer.Sound(os.path.join('sounds', 'probe_launch_1.wav'))
        self.soundTorpedo        = pygame.mixer.Sound(os.path.join('sounds', 'tos_photon_torpedo.wav'))
        self.soundKlingonTorpedo = pygame.mixer.Sound(os.path.join('sounds', 'klingon_torpedo.wav'))
        self.shieldHit           = pygame.mixer.Sound(os.path.join('sounds', 'ShieldHit.wav'))

        self.galaxyScanBackground = GalaxyScanBackground(screen=theSurface)
        self.backGround           = QuadrantBackground(theSurface)
        self.console              = StatusConsole(theSurface)

        self.gameEngine = GameEngine()
        self.enterprise = Enterprise(theSurface)

        self.galaxy   = Galaxy(theSurface, self.settings, self.intelligence, self.gameEngine)
        self.quadrant = self.galaxy.getCurrentQuadrant()

        self.statistics.currentQuadrantCoordinates = self.galaxy.currentQuadrant.coordinates
        self.statistics.currentSectorCoordinates   = self.intelligence.getRandomSectorCoordinates()
        self.quadrant.placeEnterprise(self.enterprise, self.statistics.currentSectorCoordinates)

        self.playTime = 0
        self.mouseClickEvent = None

        pygame.time.set_timer(Settings.CLOCK_EVENT, 10 * 1000)
        pygame.time.set_timer(Settings.KLINGON_TORPEDO_EVENT, 15 * 1000)

        clockCall:  UserEventCall = UserEventCall(func=StarTrekScreen.clockCB, userEvent=Settings.CLOCK_EVENT)
        ktkCall:    UserEventCall = UserEventCall(func=StarTrekScreen.ktkCB,   userEvent=Settings.KLINGON_TORPEDO_EVENT)
        entHitCall: UserEventCall = UserEventCall(func=StarTrekScreen.enterpriseTorpHitCB,
                                                  userEvent=Settings.ENTERPRISE_HIT_BY_TORPEDO_EVENT)

        RootWidget.addUserEvent(clockCall)
        RootWidget.addUserEvent(ktkCall)
        RootWidget.addUserEvent(entHitCall)
        #
        #  Init the albow widgets here
        #
        self.messageConsole = MessageConsole()
        self.add(self.messageConsole)
        StarTrekScreen._myself = self

    def key_down(self, theEvent: Event):

        self.logger.debug("key down: %s ", theEvent.key)

        if theEvent.key == pygame.K_q:
            self.ensureQuit()
        elif theEvent.key == pygame.K_g:
            self.settings.setGameMode(GameMode.GalaxyScan)
        elif theEvent.key == pygame.K_n:
            self.settings.setGameMode(GameMode.Normal)
        elif theEvent.key == pygame.K_i:
            self.settings.setGameMode(GameMode.Impulse)
        elif theEvent.key == pygame.K_t:
            self.settings.setGameMode(GameMode.PhotonTorpedoes)
        elif theEvent.key == pygame.K_s:
            self.settings.setGameMode(GameMode.SaveGame)
            self.logger.info("Saving Game")

    def mouse_down(self, theEvent: Event):

        self.logger.debug("Mouse Down")
        xPos = theEvent.pos[0]
        if xPos < StarTrekScreen.MAX_X_POS:
            self.mouseClickEvent = theEvent
            if self.settings.gameMode == GameMode.GalaxyScan:
                self.settings.gameMode = GameMode.Warp
            elif self.settings.gameMode != GameMode.Impulse:
                self.settings.gameMode = GameMode.Impulse

    def timer_event(self, theEvent: Event):
        """
        Called from the timer_event() method of the Shell when this screen is the current screen. The default
        implementation returns true so that a display update is performed.

        Args:
            theEvent:

        """
        clock = pygame.time.Clock()
        milliseconds = clock.tick(30)      # milliseconds passed since last frame; needs to agree witH StarTrekShell value
        seconds = milliseconds / 1000.0    # seconds passed since last frame (float)
        self.playTime += seconds

        return True

    def draw(self, surface: Surface):

        surface.fill(self.settings.bgColor)

        if self.settings.getGameMode() == GameMode.Normal:
            self.normalScreenUpdate(playTime=self.playTime)
        elif self.settings.getGameMode() == GameMode.Impulse:
            self.impulseScreenUpdate()
        elif self.settings.getGameMode() == GameMode.GalaxyScan:
            self.galaxyScanBackground.update(self.galaxy)
        elif self.settings.gameMode == GameMode.Warp:
            self.warpScreenUpdate()
        elif self.settings.gameMode == GameMode.PhotonTorpedoes:
            self.fireEnterpriseTorpedoesAtKlingons()

    def normalScreenUpdate(self, playTime: int):
        """"""

        self.backGround.update()
        quadrant = self.galaxy.getCurrentQuadrant()
        quadrant.update(playTime=playTime)
        self.console.update()

    def impulseScreenUpdate(self):
        """"""
        coordinates: Coordinates = self.computer.computeSectorCoordinates(self.mouseClickEvent.pos[0], self.mouseClickEvent.pos[1])
        if coordinates.__eq__(self.statistics.currentSectorCoordinates):
            self.messageConsole.addText("WTF.  You are already here!")
            self.soundUnableToComply.play()
        else:
            self.gameEngine.impulse(newCoordinates=coordinates, quadrant=self.quadrant, enterprise=self.enterprise)
            msg = f"Moved to sector: {coordinates}"
            self.messageConsole.addText(msg)
            self.soundImpulse.play()

        self.settings.gameMode = GameMode.Normal

    def warpScreenUpdate(self):
        """"""

        quadCoords: Coordinates = self.computer.computeQuadrantCoordinates(self.mouseClickEvent.pos[0], self.mouseClickEvent.pos[1])
        if quadCoords.__eq__(self.statistics.currentQuadrantCoordinates):
            self.messageConsole.addText("Hey! You are already here.")
            self.soundInaccurate.play()
        else:
            self.logger.info(f"Move to quadrant: {quadCoords}")
            #
            # Warping !!
            #
            self.quadrant = self.gameEngine.warp(moveToCoordinates=quadCoords, galaxy=self.galaxy,
                                                 intelligence=self.intelligence, enterprise=self.enterprise)
            msg = f"Warped to: {quadCoords}"
            self.messageConsole.addText(msg)
            self.soundWarp.play()

        self.settings.gameMode = GameMode.Normal

    def fireKlingonTorpedoesAtEnterprise(self):
        """"""

        quadrant = self.quadrant
        klingonCount: int = quadrant.getKlingonCount()
        if klingonCount > 0:

            self.logger.info(f"# of klingons shooting: '{klingonCount}'")
            enterprisePosition: Coordinates = self.enterprise.currentPosition
            self.logger.info(f"Enterprise is at: '{enterprisePosition}'")
            klingons: List[Klingon] = quadrant.getKlingons()
            #
            # TODO: Make random Klingons fire or maybe all fire ?
            #
            klingon:         Klingon     = klingons[0]
            klingonPosition: Coordinates = klingon.currentPosition

            self.messageConsole.addText(f"Klingon at {klingonPosition} firing!")

            torpedo: KlingonTorpedo = KlingonTorpedo(screen=self.surface,
                                                     shooterPower=klingon.getPower(),
                                                     shooterPosition=klingon.currentPosition)

            self.fireTorpedoAt(firingPosition=klingonPosition, targetPosition=enterprisePosition, torpedo=torpedo,
                               sectorType=SectorType.KLINGON_TORPEDO,
                               targetName="Enterprise", soundToPlay=self.soundKlingonTorpedo)

    def fireEnterpriseTorpedoesAtKlingons(self):
        """"""

        self.messageConsole.addText("Firing Torpedoes!!")

        quadrant:           Quadrant      = self.galaxy.getCurrentQuadrant()
        enterprisePosition: Coordinates   = self.enterprise.currentPosition

        for klingon in quadrant.klingons:

            direction: Direction = self.computer.determineDirection(enterprisePosition, klingon.currentPosition)
            torpedo: PhotonTorpedo = PhotonTorpedo(screen=self.surface, direction=direction)
            self.fireTorpedoAt(firingPosition=enterprisePosition, targetPosition=klingon.currentPosition, torpedo=torpedo,
                               sectorType=SectorType.PHOTON_TORPEDO,
                               targetName="Klingon", soundToPlay=self.soundTorpedo)

        for commander in quadrant.commanders:

            direction: Direction = self.computer.determineDirection(enterprisePosition, commander.currentPosition)
            torpedo: PhotonTorpedo = PhotonTorpedo(screen=self.surface, direction=direction)
            self.fireTorpedoAt(firingPosition=enterprisePosition, targetPosition=commander.currentPosition, torpedo=torpedo,
                               sectorType=SectorType.PHOTON_TORPEDO, targetName="Commander", soundToPlay=self.soundTorpedo)

        self.settings.gameMode = GameMode.Normal

    def fireTorpedoAt(self, firingPosition, targetPosition, torpedo, sectorType, targetName, soundToPlay):
        """

        Args:
            firingPosition:
            targetPosition:
            torpedo:
            sectorType:
            targetName:
            soundToPlay:

        """
        interceptCoordinates: List = self.computer.interpolateYIntercepts(firingPosition, targetPosition)

        self.messageConsole.addText(f"Targeting {targetName} at: {targetPosition}")

        self.logger.debug(f"{targetName} at {targetPosition}, interceptCoordinates {interceptCoordinates}")

        torpedo.setTrajectory(interceptCoordinates)

        torpedo.timeSinceMovement = self.playTime
        self.logger.debug(f"Photon Torpedo creation time {self.playTime}")

        initialTorpedoPosition: Coordinates = interceptCoordinates[0]
        self.quadrant.placeATorpedo(coordinates=initialTorpedoPosition, torpedo=torpedo, torpedoType=sectorType)
        soundToPlay.play()

    def ensureQuit(self):
        """"""
        response = ask("Quit and Save Game!", ["Yes", "Just Quit", "Cancel"])
        self.logger.info(f"response: {response}")
        if response == "Just Quit":
            self.quit()
        elif response == "Yes":
            self.saveGame()
            self.quit()

    def quit(self):
        self.logger.info("Selected Quit")
        sys.exit()

    def saveGame(self):
        self.logger.info("Selected Save Game")

    @staticmethod
    def clockCB(theEvent: Event):

        self = StarTrekScreen._myself
        self.logger.debug(f"clockEventCallback - Event Type: {theEvent.type} - relative time {theEvent.dict['time']}")

        randomTime = self.intelligence.computeRandomTimeInterval()
        self.statistics.remainingGameTime -= randomTime
        self.statistics.starDate += randomTime

    @staticmethod
    def ktkCB(theEvent: Event):

        self = StarTrekScreen._myself

        self.logger.debug(f"ktkEventCallback - Event Type: {theEvent.type} - relative time {theEvent.dict['time']}")
        self.fireKlingonTorpedoesAtEnterprise()

    @staticmethod
    def enterpriseTorpHitCB(theEvent: Event):

        self = StarTrekScreen._myself

        klingonPower:       float       = theEvent.dict['shooterPower']
        klingonPosition:    Coordinates = theEvent.dict['shooterPosition']
        enterprisePosition: Coordinates = theEvent.dict['enterprisePosition']
        self.logger.info(f"Dirty rotten Klingon{klingonPosition} shot at me {enterprisePosition} power {klingonPower}")

        hitValue: float = self.gameEngine.computeHit(shooterPosition=klingonPosition,
                                                     targetPosition=enterprisePosition,
                                                     klingonPower=klingonPower)

        shieldHitData: ShieldHitData = self.gameEngine.computeShieldHit(torpedoHit=hitValue)

        shDegradeValue = shieldHitData.shieldAbsorptionValue
        tpDegradeValue = shieldHitData.degradedTorpedoHitValue

        self.messageConsole.addText(f"Shield hit {shDegradeValue:4f}")
        self.shieldHit.play()

        self.gameEngine.degradeShields(shDegradeValue)

        self.messageConsole.addText(f"Energy hit {tpDegradeValue:4f}")
        self.gameEngine.degradeEnergyLevel(shieldHitData.degradedTorpedoHitValue)
