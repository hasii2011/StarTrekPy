import logging
import os
import sys

import pygame
import thorpy

from org.hasii.pytrek.GameMode import GameMode
from org.hasii.pytrek.Settings import Settings
from org.hasii.pytrek.engine import Direction
from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.GameEngine import GameEngine
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.gui.PhotonTorpedo import PhotonTorpedo
from org.hasii.pytrek.gui.Enterprise import Enterprise
from org.hasii.pytrek.gui.GalaxyScanBackground import GalaxyScanBackground
from org.hasii.pytrek.gui.GamePiece import GamePiece
from org.hasii.pytrek.gui.MessageWindow import MessageWindow
from org.hasii.pytrek.gui.QuadrantBackground import QuadrantBackground
from org.hasii.pytrek.gui.status.StatusConsole import StatusConsole
from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Galaxy import Galaxy

from org.hasii.pytrek.GameStatistics import GameStatistics

FLAT_BLUE_QUIT_DIALOG_TITLE_FONT_COLOR = (52,152,219)
class GameLoop():
    """"""

    LEFT_BUTTON           = 1
    MAX_X_POS             = Intelligence.GALAXY_WIDTH * GamePiece.QUADRANT_PIXEL_WIDTH
    CLOCK_EVENT           = pygame.USEREVENT + 1    # Luckily does not tromp on ThorPy
    KLINGON_TORPEDO_EVENT = CLOCK_EVENT + 1

    def __init__(self, screen: pygame.Surface):
        """"""

        self.screen               = screen

        self.settings             = Settings()
        self.computer             = Computer()
        self.stats                = GameStatistics()
        self.intelligence         = Intelligence()

        self.logger               = logging.getLogger(__name__)

        self.soundUnableToComply  = pygame.mixer.Sound(os.path.join('sounds', 'tos_unabletocomply.wav'))
        self.soundInaccurate      = pygame.mixer.Sound(os.path.join('sounds', 'tos_inaccurateerror_ep.wav'))
        self.soundWarp            = pygame.mixer.Sound(os.path.join('sounds', 'tos_flyby_1.wav'))
        self.soundImpulse         = pygame.mixer.Sound(os.path.join('sounds', 'probe_launch_1.wav'))
        self.soundTorpedo         = pygame.mixer.Sound(os.path.join('sounds', 'tos_photon_torpedo.wav'))

        self.galaxyScanBackground = GalaxyScanBackground(screen=screen)
        self.backGround           = QuadrantBackground(screen)
        self.console              = StatusConsole(screen)
        self.messageWindow        = MessageWindow(screen)

        self.gameEngine = GameEngine()

        self.galaxy     = Galaxy(screen, self.settings, self.intelligence, self.gameEngine)
        self.enterprise = Enterprise(screen)
        self.quadrant   = self.galaxy.getCurrentQuadrant()

        self.stats.currentQuadrantCoordinates = self.galaxy.currentQuadrant.coordinates
        self.stats.currentSectorCoordinates   = self.intelligence.getRandomSectorCoordinates()
        self.quadrant.placeEnterprise(self.enterprise, self.stats.currentSectorCoordinates)

    def checkPyGameEvents(self):
        """Respond to key presses and mouse events"""

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == GameLoop.CLOCK_EVENT:
                randomTime = self.intelligence.computeRandomTimeInterval()
                self.stats.remainingGameTime -= randomTime
                self.stats.starDate += randomTime
            elif event.type == GameLoop.KLINGON_TORPEDO_EVENT:
                if self.quadrant.klingonCount > 0:
                    self.logger.info("'%s': Klingons can fire torpedoes", self.quadrant.klingonCount)
                    self.fireKlingonTorpedoesAtEnterprise()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == GameLoop.LEFT_BUTTON:

                self.logger.debug(event)
                xPos = event.pos[0]
                if xPos < GameLoop.MAX_X_POS:
                    self.mouseClickEvent = event
                    if self.settings.gameMode == GameMode.GalaxyScan:
                        self.settings.gameMode = GameMode.Warp
                    elif self.settings.gameMode != GameMode.Impulse:
                        self.settings.gameMode = GameMode.Impulse
            elif event.type == pygame.KEYDOWN:

                if (self.settings.getGameMode() == GameMode.Impulse and event.key == pygame.K_RETURN):
                    self.settings.setGameMode(GameMode.Normal)
                elif self.settings.getGameMode() != GameMode.Impulse:
                    self.checkKeyDownEvents(event)

        self.events = events

    def updateScreen(self, playTime: int):
        """Update screen images and flip to the new screens"""

        self.screen.fill(self.settings.bgColor)

        if self.settings.getGameMode()   == GameMode.Normal:
            self.normalScreenUpdate(playTime=playTime)
        elif self.settings.getGameMode() == GameMode.GalaxyScan:
            self.galaxyScanBackground.update(self.galaxy)
        elif self.settings.getGameMode() == GameMode.Impulse:
            self.impulseScreenUpdate()
        elif self.settings.gameMode      == GameMode.Warp:
            self.warpScreenUpdate()
        elif self.settings.gameMode      == GameMode.PhotonTorpedoes:
            self.fireEnterpriseTorpedoesAtKlingons(playTime)

        pygame.display.flip()

    def checkKeyDownEvents(self, event):
        """Respond to key presses"""

        self.logger.debug("key down: %s ",  event.key)

        if event.key == pygame.K_q:
            self.ensureQuit()
        elif event.key == pygame.K_g:
            self.settings.setGameMode(GameMode.GalaxyScan)
        elif event.key == pygame.K_n:
            self.settings.setGameMode(GameMode.Normal)
        elif event.key == pygame.K_i:
            self.settings.setGameMode(GameMode.Impulse)
        elif event.key == pygame.K_t:
            self.settings.setGameMode(GameMode.PhotonTorpedoes)
        elif event.key == pygame.K_s:
            self.settings.setGameMode(GameMode.SaveGame)
            self.logger.info("Saving Game")

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
        if coordinates.__eq__(self.stats.currentSectorCoordinates):
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
        if quadrantCoordinates.__eq__(self.stats.currentQuadrantCoordinates):
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
        direction:            Direction   = self.computer.determineDirection(enterprisePosition, badGuyPosition)
        interceptCoordinates: Coordinates = self.computer.interpolateYIntercepts(enterprisePosition, badGuyPosition)

        self.messageWindow.displayMessage("Targeting " + badGuyName + " at: " + badGuyPosition.__str__())

        self.logger.debug("%s at %s, Shooting Direction: %s, interceptCoordinates %s", badGuyName, badGuyPosition, direction.name, interceptCoordinates)

        torpedo: PhotonTorpedo = PhotonTorpedo(screen=self.screen, direction=direction)
        torpedo.setTrajectory(interceptCoordinates)
        torpedo.timeSinceMovement = playTime
        self.logger.debug("Photon Torpedo creation time %s", playTime)

        initialTorpedoPosition: Coordinates = interceptCoordinates[0]
        self.quadrant.placeATorpedo(coordinates=initialTorpedoPosition, torpedo=torpedo)
        self.soundTorpedo.play()

    def ensureQuit(self):
        """"""
        thorpy.set_theme("human")
        choices = [(thorpy.style.OK_TXT, self.saveGame), ("Just Quit", self.quit),(thorpy.style.CANCEL_TXT, None)]
        thorpy.launch_blocking_choices(text="Quit and Save Game!\n", choices=choices,
                                    title_fontcolor=FLAT_BLUE_QUIT_DIALOG_TITLE_FONT_COLOR,
                                    title_fontsize=16,
                                    parent=None)
        self.logger.info("After unblocked choices")

    def quit(self):
        self.logger.info("Selected Quit")
        sys.exit()
    def saveGame(self):
        self.logger.info("Selected Save Game")