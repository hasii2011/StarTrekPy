
import logging

import pygame

from pygame.sprite import Sprite

from org.hasii.pytrek.Settings import WHITE
from org.hasii.pytrek.Settings import GREEN
from org.hasii.pytrek.Settings import RED


from org.hasii.pytrek.engine.ShieldStatus import ShieldStatus
from org.hasii.pytrek.engine.PhaserStatus import PhaserStatus
from org.hasii.pytrek.engine.TorpedoStatus import TorpedoStatus
from org.hasii.pytrek.engine.ComputerStatus import ComputerStatus

from org.hasii.pytrek.gui.status.StatusRenderer import StatusRenderer
from org.hasii.pytrek.gui.status.StatusRenderer import LABEL_X

from org.hasii.pytrek.GameStatistics import GameStatistics

Y_TITLE_OFFSET       = 12
Y_LABEL_START_OFFSET = 64
Y_LABEL_INCREMENT    = 18

STAR_DATE_Y       = Y_LABEL_START_OFFSET
QUADRANT_Y        = STAR_DATE_Y       + Y_LABEL_INCREMENT
SECTOR_Y          = QUADRANT_Y        + Y_LABEL_INCREMENT
ENERGY_Y          = SECTOR_Y          + Y_LABEL_INCREMENT
SHIELD_ENERGY_Y   = ENERGY_Y          + Y_LABEL_INCREMENT
REM_GAME_Y        = SHIELD_ENERGY_Y   + Y_LABEL_INCREMENT
KLINGON_COUNT_Y   = REM_GAME_Y        + Y_LABEL_INCREMENT
COMMANDER_COUNT_Y = KLINGON_COUNT_Y   + Y_LABEL_INCREMENT

SYSTEM_STATUS_Y     = COMMANDER_COUNT_Y + Y_LABEL_INCREMENT + Y_LABEL_INCREMENT
SHIELD_STATUS_Y     = SYSTEM_STATUS_Y   + Y_LABEL_INCREMENT
PHASER_STATUS_Y     = SHIELD_STATUS_Y   + Y_LABEL_INCREMENT
TORPEDO_STATUS_Y    = PHASER_STATUS_Y   + Y_LABEL_INCREMENT
COMPUTER_STATUS_Y   = TORPEDO_STATUS_Y  + Y_LABEL_INCREMENT

FONT_PATH = "fonts/MonoFonto.ttf"


class StatusConsole(Sprite):
    """ UI portion of status console"""

    def __init__(self, screen):
        """"""
        super().__init__()
        self.screen   = screen

        self.stats    = GameStatistics()

        self.logger = logging.getLogger(__name__)
        self.titleX = LABEL_X
        self.titleY = Y_TITLE_OFFSET

        self.consoleLabelFont      = pygame.font.Font(FONT_PATH, 20)
        self.statusFont            = pygame.font.Font(FONT_PATH, 14)
        self.systemStatusLabelFont = pygame.font.Font(FONT_PATH, 16)

        self.systemStatusLabelFont.set_underline(True)

        self.consoleLabel = self.consoleLabelFont.render("Status Console", 1, WHITE)

        self.starDateStatus: StatusRenderer = StatusRenderer(screen, "Stardate:",   STAR_DATE_Y)
        self.quadrantStatus: StatusRenderer = StatusRenderer(screen, "Quadrant:",   QUADRANT_Y)
        self.sectorStatus:   StatusRenderer = StatusRenderer(screen, "Sector:",     SECTOR_Y)
        self.energyStatus:   StatusRenderer = StatusRenderer(screen, "Energy:",     ENERGY_Y)
        self.shieldEnergy:   StatusRenderer = StatusRenderer(screen, "Shields:",    SHIELD_ENERGY_Y)
        self.remGameTime:    StatusRenderer = StatusRenderer(screen, "Game Time:",  REM_GAME_Y)
        self.klingonCount:   StatusRenderer = StatusRenderer(screen, "Klingons:",   KLINGON_COUNT_Y)
        self.commanderCount: StatusRenderer = StatusRenderer(screen, "Commanders:", COMMANDER_COUNT_Y)

        self.systemsStatusLabel   = self.systemStatusLabelFont.render("SYSTEMS ", 1, WHITE)

        self.shieldStatus:   StatusRenderer = StatusRenderer(screen, "Shields:",  SHIELD_STATUS_Y)
        self.phaserStatus:   StatusRenderer = StatusRenderer(screen, "Phasers:",  PHASER_STATUS_Y)
        self.torpedoStatus:  StatusRenderer = StatusRenderer(screen, "Torpedos:", TORPEDO_STATUS_Y)
        self.computerStatus: StatusRenderer = StatusRenderer(screen, "Computer:", COMPUTER_STATUS_Y)

        self.computerStatusLabel  = self.statusFont.render("Computer: ", 1, WHITE)

    def update(self):
        """"""

        self.updateGameSettings()
        self.updateSystemsStatus()

    def updateGameSettings(self):

        formattedStarDate       = "{:8.2f}".format(self.stats.starDate)
        formattedEnergy         = "{:7.2f}".format(self.stats.energy)
        formattedShieldEnergy   = "{:7.2f}".format(self.stats.shieldEnergy)
        formattedRemGameTime    = "{:6.2f}".format(self.stats.remainingGameTime)

        self.screen.blit(self.consoleLabel, (self.titleX, self.titleY))

        self.starDateStatus.display(formattedStarDate, WHITE)
        self.quadrantStatus.display(str(self.stats.currentQuadrantCoordinates), WHITE)
        self.sectorStatus.display(str(self.stats.currentSectorCoordinates), WHITE)
        self.energyStatus.display(formattedEnergy, WHITE)
        self.shieldEnergy.display(formattedShieldEnergy, WHITE)
        self.remGameTime.display(formattedRemGameTime, WHITE)
        self.klingonCount.display(str(self.stats.remainingKlingons), WHITE)
        self.commanderCount.display(str(self.stats.remainingCommanders), WHITE)

    def updateSystemsStatus(self):
        """
        """
        self.screen.blit(self.systemsStatusLabel, (LABEL_X, SYSTEM_STATUS_Y))

        statusColor = GREEN if self.stats.shieldStatus == ShieldStatus.Up else RED
        self.shieldStatus.display(self.stats.shieldStatus.name, statusColor)

        statusColor = GREEN if self.stats.phaserStatus == PhaserStatus.Up else RED
        self.phaserStatus.display(self.stats.phaserStatus.name, statusColor)

        statusColor = GREEN if self.stats.torpedoStatus == TorpedoStatus.Up else RED
        self.torpedoStatus.display(self.stats.torpedoStatus.name, statusColor)

        statusColor = GREEN if self.stats.computerStatus == ComputerStatus.Up else RED
        self.computerStatus.display(self.stats.computerStatus.name, statusColor)
