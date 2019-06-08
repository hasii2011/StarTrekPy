
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
from albow.core.ui.AlbowEventLoop import AlbowEventLoop
from albow.core.UserEventCall import UserEventCall

from albow.dialog.DialogUtilities import ask

from org.hasii.pytrek.GameStatistics import GameStatistics
from org.hasii.pytrek.GameMode import GameMode
from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Galaxy import Galaxy


from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.engine import Direction

from org.hasii.pytrek.gui.Enterprise import Enterprise
from org.hasii.pytrek.gui.GalaxyScanBackground import GalaxyScanBackground
from org.hasii.pytrek.gui.MessageWindow import MessageWindow
from org.hasii.pytrek.gui.QuadrantBackground import QuadrantBackground
from org.hasii.pytrek.gui.status.StatusConsole import StatusConsole
from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.gui.PhotonTorpedo import PhotonTorpedo


class StarTrekScreen(Screen):

    MAX_X_POS = Intelligence.GALAXY_WIDTH * GamePiece.QUADRANT_PIXEL_WIDTH

    CLOCK_EVENT = AlbowEventLoop.MUSIC_END_EVENT + 1
    KLINGON_TORPEDO_EVENT = CLOCK_EVENT + 1

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

        self.galaxyScanBackground = GalaxyScanBackground(screen=theSurface)
        self.backGround           = QuadrantBackground(theSurface)
        self.console              = StatusConsole(theSurface)
        self.messageWindow        = MessageWindow(theSurface)

        self.gameEngine = GameEngine()
        self.enterprise = Enterprise(theSurface)

        self.galaxy   = Galaxy(theSurface, self.settings, self.intelligence, self.gameEngine)
        self.quadrant = self.galaxy.getCurrentQuadrant()

        self.statistics.currentQuadrantCoordinates = self.galaxy.currentQuadrant.coordinates
        self.statistics.currentSectorCoordinates   = self.intelligence.getRandomSectorCoordinates()
        self.quadrant.placeEnterprise(self.enterprise, self.statistics.currentSectorCoordinates)

        self.playTime = 0
        self.mouseClickEvent = None

        pygame.time.set_timer(StarTrekScreen.CLOCK_EVENT, 10 * 1000)
        pygame.time.set_timer(StarTrekScreen.KLINGON_TORPEDO_EVENT, 15 * 1000)

        clockEventCall: UserEventCall = UserEventCall(func=StarTrekScreen.clockEventCallback, userEvent=StarTrekScreen.CLOCK_EVENT)
        ktkEventCall: UserEventCall = UserEventCall(func=StarTrekScreen.ktkEventCallback, userEvent=StarTrekScreen.KLINGON_TORPEDO_EVENT)

        RootWidget.addUserEvent(clockEventCall)
        RootWidget.addUserEvent(ktkEventCall)

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

        self.logger.info("Mouse Down")
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
            self.fireEnterpriseTorpedoesAtKlingons(playTime=self.playTime)

    def normalScreenUpdate(self, playTime: int):
        """"""

        self.backGround.update()
        quadrant = self.galaxy.getCurrentQuadrant()
        quadrant.update(playTime=playTime)
        self.console.update()
        self.messageWindow.update()

    def impulseScreenUpdate(self):
        """"""
        coordinates: Coordinates = self.computer.computeSectorCoordinates(self.mouseClickEvent.pos[0], self.mouseClickEvent.pos[1])
        if coordinates.__eq__(self.statistics.currentSectorCoordinates):
            self.messageWindow.displayMessage("WTF.  You are already here!")
            self.soundUnableToComply.play()
        else:
            self.gameEngine.impulse(newCoordinates=coordinates, quadrant=self.quadrant, enterprise=self.enterprise)
            self.messageWindow.displayMessage("Moved to sector: " + coordinates.__str__())
            self.soundImpulse.play()

        self.settings.gameMode = GameMode.Normal

    def warpScreenUpdate(self):
        """"""

        quadrantCoordinates: Coordinates = self.computer.computeQuadrantCoordinates(self.mouseClickEvent.pos[0], self.mouseClickEvent.pos[1])
        if quadrantCoordinates.__eq__(self.statistics.currentQuadrantCoordinates):
            self.messageWindow.displayMessage("Hey! You are already here.")
            self.soundInaccurate.play()
        else:
            self.logger.info("Move to quadrant: %s", quadrantCoordinates)
            #
            # Warping !!
            #
            self.quadrant = self.gameEngine.warp(moveToCoordinates=quadrantCoordinates, galaxy=self.galaxy,
                                                 intelligence=self.intelligence, enterprise=self.enterprise)
            self.messageWindow.displayMessage("Warped to: " + quadrantCoordinates.__str__())
            self.soundWarp.play()

        self.settings.gameMode = GameMode.Normal

    def fireKlingonTorpedoesAtEnterprise(self):
        """"""

        enterprisePosition: Coordinates = self.enterprise.currentPosition
        self.logger.info("Enterprise is at: '%s'", enterprisePosition)

    def fireEnterpriseTorpedoesAtKlingons(self, playTime: int):
        """"""

        self.messageWindow.displayMessage("Firing Torpedoes!!")

        quadrant = self.galaxy.getCurrentQuadrant()

        enterprisePosition: Coordinates = quadrant.enterpriseCoordinates

        for klingon in quadrant.klingons:
            self.fireTorpedoAt(klingon, enterprisePosition, playTime, "Klingon")

        for commander in quadrant.commanders:
            self.fireTorpedoAt(commander, enterprisePosition, playTime, "Commander")

        self.settings.gameMode = GameMode.Normal

    def fireTorpedoAt(self, badGuy, enterprisePosition, playTime, badGuyName):
        """"""

        badGuyPosition:       Coordinates = badGuy.currentPosition
        interceptCoordinates: List = self.computer.interpolateYIntercepts(enterprisePosition, badGuyPosition)
        direction:            Direction = self.computer.determineDirection(enterprisePosition, badGuyPosition)

        self.messageWindow.displayMessage("Targeting " + badGuyName + " at: " + badGuyPosition.__str__())

        self.logger.debug("%s at %s, Shooting Direction: %s, interceptCoordinates %s", badGuyName, badGuyPosition, direction.name, interceptCoordinates)

        torpedo: PhotonTorpedo = PhotonTorpedo(screen=self.surface, direction=direction)
        torpedo.setTrajectory(interceptCoordinates)
        torpedo.timeSinceMovement = playTime
        self.logger.debug("Photon Torpedo creation time %s", playTime)

        initialTorpedoPosition: Coordinates = interceptCoordinates[0]
        self.quadrant.placeATorpedo(coordinates=initialTorpedoPosition, torpedo=torpedo)
        self.soundTorpedo.play()

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
    def clockEventCallback(theEvent: Event):

        self = StarTrekScreen._myself
        self.logger.info(f"Event Type: {theEvent.type} - relative time {theEvent.dict['time']}")

        randomTime = self.intelligence.computeRandomTimeInterval()
        self.statistics.remainingGameTime -= randomTime
        self.statistics.starDate += randomTime

    @staticmethod
    def ktkEventCallback(theEvent: Event):

        self = StarTrekScreen._myself

        self.logger.info(f"Event Type: {theEvent.type} - relative time {theEvent.dict['time']}")
        self.fireKlingonTorpedoesAtEnterprise()
