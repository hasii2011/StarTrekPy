
import sys

import os

import logging
from logging import Logger

from typing import List

import pygame

from pygame import Surface
from pygame.mixer import Sound

from pygame.event import Event

from albow.core.ui.Screen import Screen
from albow.core.ui.Shell import Shell
from albow.core.ui.RootWidget import RootWidget
from albow.core.UserEventCall import UserEventCall

from albow.dialog.DialogUtilities import ask
from albow.dialog.DialogUtilities import alert

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
from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.DeviceType import DeviceType
from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus
from org.hasii.pytrek.engine.ShieldHitData import ShieldHitData
from org.hasii.pytrek.engine.ShipCondition import ShipCondition

from org.hasii.pytrek.gui.GalaxyScanBackground import GalaxyScanBackground
from org.hasii.pytrek.gui.MessageConsole import MessageConsole
from org.hasii.pytrek.gui.QuadrantBackground import QuadrantBackground
from org.hasii.pytrek.gui.StatusConsole import StatusConsole

from org.hasii.pytrek.gui.gamepieces.Enterprise import Enterprise
from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece
from org.hasii.pytrek.gui.gamepieces.Klingon import Klingon
from org.hasii.pytrek.gui.gamepieces.PhotonTorpedo import PhotonTorpedo
from org.hasii.pytrek.gui.gamepieces.KlingonTorpedo import KlingonTorpedo

MSG_IMPULSE_ENGINES_ARE_DOWN = 'Sorry, Impulse Engines are down.'
MSG_WARP_ENGINES_ARE_DOWN    = 'Apologies, Warp Engines are damaged.'


class StarTrekScreen(Screen):

    MAX_X_POS = Intelligence.GALAXY_WIDTH * GamePiece.QUADRANT_PIXEL_WIDTH

    KLINGON_TORPEDO_EVENT_SECS = 15 * 1000

    _myself: 'StarTrekScreen' = None

    def __init__(self, shell: Shell, theSurface: Surface):

        super().__init__(shell)

        self.logger: Logger = logging.getLogger(__name__)
        #
        # Debug logger
        #
        # saveLogger = self.logger
        # while self.logger is not None:
        #     print(f"level: '{self.logger.level}'', name: '{self.logger.name}'', handlers: '{self.logger.handlers}"'')
        #     self.logger = self.logger.parent
        # self.logger = saveLogger
        #
        self.surface: Surface = theSurface

        self.settings: Settings = Settings()
        self.computer: Computer = Computer()

        self.statistics:   GameStatistics = GameStatistics()
        self.intelligence: Intelligence   = Intelligence()
        self.devices:      Devices        = Devices()

        self.soundUnableToComply: Sound = pygame.mixer.Sound(os.path.join('sounds', 'tos_unabletocomply.wav'))
        self.soundInaccurate:     Sound = pygame.mixer.Sound(os.path.join('sounds', 'tos_inaccurateerror_ep.wav'))
        self.soundWarp:           Sound = pygame.mixer.Sound(os.path.join('sounds', 'tos_flyby_1.wav'))
        self.soundImpulse:        Sound = pygame.mixer.Sound(os.path.join('sounds', 'probe_launch_1.wav'))
        self.soundTorpedo:        Sound = pygame.mixer.Sound(os.path.join('sounds', 'tos_photon_torpedo.wav'))
        self.soundKlingonTorpedo: Sound = pygame.mixer.Sound(os.path.join('sounds', 'klingon_torpedo.wav'))
        self.soundShieldHit:      Sound = pygame.mixer.Sound(os.path.join('sounds', 'ShieldHit.wav'))
        self.soundDeviceDown:     Sound = pygame.mixer.Sound(os.path.join('sounds', 'tng_red_alert2.wav'))

        self.galaxyScanBackground: GalaxyScanBackground = GalaxyScanBackground(screen=theSurface)
        self.backGround:           QuadrantBackground   = QuadrantBackground(theSurface)

        self.gameEngine: GameEngine = GameEngine()
        self.enterprise: Enterprise = Enterprise(theSurface)

        self.galaxy:   Galaxy   = Galaxy(screen=theSurface, intelligence=self.intelligence, gameEngine=self.gameEngine)
        self.quadrant: Quadrant = self.galaxy.getCurrentQuadrant()

        self.statistics.currentQuadrantCoordinates = self.galaxy.currentQuadrant.coordinates
        self.statistics.currentSectorCoordinates   = self.intelligence.getRandomSectorCoordinates()
        self.quadrant.placeEnterprise(self.enterprise, self.statistics.currentSectorCoordinates)

        self.playTime:        float = 0.0
        self.mouseClickEvent: Event = None

        pygame.time.set_timer(Settings.CLOCK_EVENT, 10 * 1000)
        pygame.time.set_timer(Settings.KLINGON_TORPEDO_EVENT, StarTrekScreen.KLINGON_TORPEDO_EVENT_SECS)

        clockCall:  UserEventCall = UserEventCall(func=StarTrekScreen.clockCB, userEvent=Settings.CLOCK_EVENT)
        ktkCall:    UserEventCall = UserEventCall(func=StarTrekScreen.ktkCB,   userEvent=Settings.KLINGON_TORPEDO_EVENT)
        entHitCall: UserEventCall = UserEventCall(func=StarTrekScreen.enterpriseHitCB,
                                                  userEvent=Settings.ENTERPRISE_HIT_BY_TORPEDO_EVENT)

        RootWidget.addUserEvent(clockCall)
        RootWidget.addUserEvent(ktkCall)
        RootWidget.addUserEvent(entHitCall)
        #
        #  Init the albow widgets here
        #
        self.messageConsole = MessageConsole()
        self.statusConsole  = StatusConsole()

        self.add(self.messageConsole)
        self.add(self.statusConsole)
        StarTrekScreen._myself = self

    def key_down(self, theEvent: Event):

        self.logger.debug(f"key down: {theEvent.key}")

        if theEvent.key == pygame.K_q:
            self.ensureQuit()
        elif theEvent.key == pygame.K_g:
            status: DeviceStatus = self.devices.getDeviceStatus(DeviceType.SubspaceRadio)
            if status == DeviceStatus.Up:
                self.settings.setGameMode(GameMode.GalaxyScan)
            else:
                self.messageConsole.addText("Sorry, The subspace radio is down.")
                self.soundDeviceDown.play()
        elif theEvent.key == pygame.K_n:
            self.settings.setGameMode(GameMode.Normal)
        elif theEvent.key == pygame.K_i:
            status: DeviceStatus = self.devices.getDevice(DeviceType.ImpulseEngines).getDeviceStatus()
            if status == DeviceStatus.Up:
                self.settings.setGameMode(GameMode.Impulse)
            else:
                self.messageConsole.addText(MSG_IMPULSE_ENGINES_ARE_DOWN)
                self.soundDeviceDown.play()
        elif theEvent.key == pygame.K_t:
            status: DeviceStatus = self.devices.getDeviceStatus(DeviceType.PhotonTubes)
            if status == DeviceStatus.Up:
                self.settings.setGameMode(GameMode.PhotonTorpedoes)
            else:
                self.messageConsole.addText("Sorry, Photon Tubes are down.")
                self.soundDeviceDown.play()

        elif theEvent.key == pygame.K_s:
            self.settings.setGameMode(GameMode.SaveGame)
            self.logger.info("Saving Game")

    def mouse_down(self, theEvent: Event):

        self.logger.debug("Mouse Pressed Down")
        xPos = theEvent.pos[0]
        if xPos < StarTrekScreen.MAX_X_POS:
            self.mouseClickEvent = theEvent
            if self.settings.gameMode == GameMode.GalaxyScan:
                status: DeviceStatus = self.devices.getDeviceStatus(DeviceType.WarpEngines)
                if status == DeviceStatus.Up:
                    self.settings.gameMode = GameMode.Warp
                    self._cancelKlingonTorpedoEvent()
                else:
                    self.messageConsole.addText(MSG_WARP_ENGINES_ARE_DOWN)
                    self.soundDeviceDown.play()
            elif self.settings.gameMode != GameMode.Impulse:
                status: DeviceStatus = self.devices.getDeviceStatus(DeviceType.ImpulseEngines)
                if status == DeviceStatus.Up:
                    self.settings.gameMode = GameMode.Impulse
                else:
                    self.messageConsole.addText(MSG_IMPULSE_ENGINES_ARE_DOWN)
                    self.soundDeviceDown.play()

    def timer_event(self, theEvent: Event):
        """
        Called from the timer_event() method of the Shell when this screen is the current screen. The default
        implementation returns true so that a display update is performed.

        Args:
            theEvent:

        """
        clock          = pygame.time.Clock()
        milliseconds   = clock.tick(30)         # milliseconds passed since last frame; needs to agree witH StarTrekShell value
        quarterSeconds = milliseconds / 250.0   # quarter-seconds passed since last frame (float)
        self.playTime  += quarterSeconds

        StarTrekScreen.quitIfTimeExpired()

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

    def normalScreenUpdate(self, playTime: float):
        """"""

        self.backGround.update()
        quadrant = self.galaxy.getCurrentQuadrant()
        quadrant.update(playTime=playTime)

    def impulseScreenUpdate(self):
        """"""
        coordinates: Coordinates = self.computer.computeSectorCoordinates(self.mouseClickEvent.pos[0], self.mouseClickEvent.pos[1])
        if coordinates.__eq__(self.statistics.currentSectorCoordinates):
            self.messageConsole.addText("WTF.  You are already here!")
            self.soundUnableToComply.play()
        else:
            self.gameEngine.impulse(newCoordinates=coordinates, quadrant=self.quadrant, enterprise=self.enterprise)

            self.messageConsole.addText(f"Moved to sector: {coordinates}")
            self.soundImpulse.play()

        StarTrekScreen.quitIfTimeExpired()
        self._dockIfAdjacentToStarbase()
        self.settings.gameMode = GameMode.Normal

    def warpScreenUpdate(self):
        """"""

        quadCoords: Coordinates = self.computer.computeQuadrantCoordinates(self.mouseClickEvent.pos[0], self.mouseClickEvent.pos[1])
        if quadCoords.__eq__(self.statistics.currentQuadrantCoordinates):
            self.messageConsole.addText("Hey! You are already here.")
            self.soundInaccurate.play()
        else:
            #
            # Warping !!
            #
            self.logger.info(f"Move to quadrant: {quadCoords}")
            self.quadrant = self.gameEngine.warp(moveToCoordinates=quadCoords, galaxy=self.galaxy,
                                                 intelligence=self.intelligence, enterprise=self.enterprise)

            self.messageConsole.addText(f"Warped to: {quadCoords}")
            self.soundWarp.play()

        StarTrekScreen.quitIfTimeExpired()
        self._dockIfAdjacentToStarbase()
        self.settings.gameMode = GameMode.Normal
        self._restartKlingonTorpedoEvent()

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

    def _cancelKlingonTorpedoEvent(self):
        pygame.time.set_timer(Settings.KLINGON_TORPEDO_EVENT, 0)

    def _restartKlingonTorpedoEvent(self):
        pygame.time.set_timer(Settings.KLINGON_TORPEDO_EVENT, StarTrekScreen.KLINGON_TORPEDO_EVENT_SECS)

    def _dockIfAdjacentToStarbase(self):

        currentQuadrant: Quadrant = self.galaxy.currentQuadrant
        if currentQuadrant.hasStarBase() is True:
            currentQuadrant: Quadrant = self.galaxy.currentQuadrant
            enterpriseCoords: Coordinates = currentQuadrant.enterpriseCoordinates
            starBaseCoords: Coordinates = currentQuadrant.starBaseCoords

            if self.gameEngine.isShipAdjacentToBase(enterpriseLoc=enterpriseCoords, starbaseLoc=starBaseCoords) is True:
                self.gameEngine.dock()
                self.messageConsole.addText(f"Docked with starbase at: {starBaseCoords}")
        else:
            self._determineShipCondition(self.galaxy.getCurrentQuadrant())

    def _determineShipCondition(self, quadrant: Quadrant):
        """
        Called when we know we are NOT docked

        TODO:  What determines the other conditions, Yellow and Red
        From the java version Space War it seems like
        Yellow:
            ships energy is less than 1000
        """
        self.statistics.shipCondition = ShipCondition.Green
        if self.statistics.energy < 1000:
            self.statistics.shipCondition = ShipCondition.Yellow
        if quadrant.getKlingonCount() > 0 or quadrant.getCommanderCount() > 0 or \
        quadrant.getRomulanCount() > 0 or quadrant.getSuperCommanderCount() > 0:
            self.statistics.shipCondition = ShipCondition.Red

    @staticmethod
    def clockCB(theEvent: Event):

        self = StarTrekScreen._myself
        self.logger.debug(f"clockEventCallback - Event Type: {theEvent.type} - relative time {theEvent.dict['time']}")

        randomTime = self.intelligence.computeRandomTimeInterval()
        self.statistics.remainingGameTime -= randomTime
        self.statistics.starDate += randomTime
        StarTrekScreen.quitIfTimeExpired()

    @staticmethod
    def ktkCB(theEvent: Event):

        self = StarTrekScreen._myself

        self.logger.debug(f"ktkEventCallback - Event Type: {theEvent.type} - relative time {theEvent.dict['time']}")
        self.fireKlingonTorpedoesAtEnterprise()

    @staticmethod
    def enterpriseHitCB(theEvent: Event):

        self = StarTrekScreen._myself

        klingonPower:       float       = theEvent.dict['shooterPower']
        klingonPosition:    Coordinates = theEvent.dict['shooterPosition']
        enterprisePosition: Coordinates = theEvent.dict['enterprisePosition']
        self.logger.info(f"Dirty rotten Klingon{klingonPosition} shot at me {enterprisePosition} power {klingonPower}")

        hitValue: float = self.gameEngine.computeHit(shooterPosition=klingonPosition,
                                                     targetPosition=enterprisePosition,
                                                     klingonPower=klingonPower)

        self.logger.debug(f"Original Hit Value: {hitValue:4f}")
        if self.devices.getDeviceStatus(DeviceType.Shields) == DeviceStatus.Up:
            shieldHitData: ShieldHitData = self.gameEngine.computeShieldHit(torpedoHit=hitValue)
        else:
            shieldHitData: ShieldHitData = ShieldHitData(degradedTorpedoHitValue=hitValue, shieldAbsorptionValue=0.0)

        shieldAbsorptionValue   = shieldHitData.shieldAbsorptionValue
        degradedTorpedoHitValue = shieldHitData.degradedTorpedoHitValue

        self.messageConsole.addText(f"Shield Hit: {shieldAbsorptionValue:4f}  Enterprise hit: {degradedTorpedoHitValue:4f}")
        self.soundShieldHit.play()
        self.gameEngine.degradeShields(shieldAbsorptionValue)

        self.gameEngine.degradeEnergyLevel(shieldHitData.degradedTorpedoHitValue)
        if self.statistics.energy <= 0:
            alert(theMessage='Game Over!  The Enterprise is out of energy')
            sys.exit()

        damagedDeviceType: DeviceType = self.intelligence.fryDevice(shieldHitData.degradedTorpedoHitValue)
        if damagedDeviceType is not None:
            self.messageConsole.addText(f"Device: {damagedDeviceType} damaged")

        if damagedDeviceType == DeviceType.Shields:
            self.messageConsole.addText("Shield energy transferred to Enterprise")
            self.statistics.energy += self.statistics.shieldEnergy
            self.statistics.shieldEnergy = 0

    @staticmethod
    def quitIfTimeExpired():

        self = StarTrekScreen._myself
        if self.statistics.remainingGameTime <= 0:
            enemyCount = self.statistics.getRemainingKlingons() + self.statistics.getRemainingCommanders()
            msg = (
                f"It is stardate {self.statistics.starDate:6.2f} "
                f"the game time has expired.  "
                f"You still have {enemyCount} enemies remaining"
            )
            alert(theMessage=msg, theWrapWidth=50)
            sys.exit()
