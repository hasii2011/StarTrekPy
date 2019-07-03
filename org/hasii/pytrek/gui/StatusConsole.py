
import pygame

import logging

from albow.themes.Theme import Theme

from albow.core.ui.Widget import Widget

from albow.layout.Column import Column
from albow.layout.Grid import Grid

from albow.widgets.Label import Label
from albow.widgets.ValueDisplay import ValueDisplay

from albow.References import AttrRef

from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.GameStatistics import GameStatistics

from org.hasii.pytrek.engine.Devices import Devices
from org.hasii.pytrek.engine.DeviceType import DeviceType

from org.hasii.pytrek.gui.DamageValueDisplay import DamageValueDisplay


class StatusConsole(Widget):

    FONT_PATH = "fonts/MonoFonto.ttf"

    def __init__(self, **kwds):

        super().__init__(**kwds)

        self.logger = logging.getLogger(__name__)

        self.consoleLabelFont      = pygame.font.Font(StatusConsole.FONT_PATH, 20)
        self.statusFont            = pygame.font.Font(StatusConsole.FONT_PATH, 14)
        self.systemStatusLabelFont = pygame.font.Font(StatusConsole.FONT_PATH, 16)

        self.settings:       Settings       = Settings()
        self.gameStatistics: GameStatistics = GameStatistics()
        self.devices:        Devices        = Devices()

        self._customizeConsoleContainer()

        consoleLabel: Label = self._makeStatusSectionLabel()
        statusGrid:   Grid  = self._makeStatusGrid()
        systemsLabel: Label = self._makeSystemStatusSectionLabel()
        systemsGrid:  Grid  = self._makeSystemsGrid()

        contentAttrs = {
            'align':        'c',
            'expand':       1,
            'equalize':     'w',
            'bg_color':     Theme.BLACK,
            'border_color': Theme.LAMAS_DARK_BLUE,
            'border_width': 1,
            'margin':       6
        }
        contents: Column = Column([consoleLabel, statusGrid, systemsLabel, systemsGrid], **contentAttrs)
        self.add_centered(contents)

    def _makeStatusSectionLabel(self):
        return self._makeSectionLabel("Status Console")

    def _makeSystemStatusSectionLabel(self):
        return self._makeSectionLabel("SYSTEMS")

    def _makeSectionLabel(self, labelText: str):

        consoleLabelAttrs = {
            'bg_color': Theme.BLACK,
            'fg_color': Theme.WHITE,
            'font':     self.consoleLabelFont
        }
        sectionLabel: Label = Label(labelText, **consoleLabelAttrs)
        return sectionLabel

    def _makeStatusGrid(self) -> Grid:

        labels = [
            'StarDate: ',
            'Quadrant: ',
            'Sector: ',
            'Energy: ',
            'Shields: ',
            'Game Time: ',
            'Klingons:',
            'Commanders:'
        ]
        refs = [
            AttrRef(base=self.gameStatistics, name="starDate"),
            AttrRef(base=self.gameStatistics, name="currentQuadrantCoordinates"),
            AttrRef(base=self.gameStatistics, name="currentSectorCoordinates"),
            AttrRef(base=self.gameStatistics, name="energy"),
            AttrRef(base=self.gameStatistics, name="shieldEnergy"),
            AttrRef(base=self.gameStatistics, name="remainingGameTime"),
            AttrRef(base=self.gameStatistics, name="remainingKlingons"),
            AttrRef(base=self.gameStatistics, name="remainingCommanders"),
        ]
        formatStrs = [
            '%8.2f',
            None,
            None,
            '%7.2f',
            '%7.2f',
            '%6.2f',
            None,
            None,
        ]
        statusItems = []
        for x in range(len(labels)):
            fieldContent = self._makeStatusRow(labels[x], refs[x], formatStrs[x])
            statusItems.append(fieldContent)
        statusGridAttrs = {
            'bg_color':     Theme.BLACK,
            'border_color': Theme.LAMAS_MEDIUM_BLUE,
        }
        statusGrid: Grid = Grid(rows=statusItems, column_spacing=5, row_spacing=2, **statusGridAttrs)
        return statusGrid

    def _makeSystemsGrid(self) -> Grid:

        labels = [
            'Shields: ',
            'Phasers: ',
            'Torpedos: ',
            'Computer: '
        ]
        refs = [
            AttrRef(base=self.devices.getDevice(DeviceType.Shields),     name="deviceStatus"),
            AttrRef(base=self.devices.getDevice(DeviceType.Phasers),     name="deviceStatus"),
            AttrRef(base=self.devices.getDevice(DeviceType.PhotonTubes), name="deviceStatus"),
            AttrRef(base=self.devices.getDevice(DeviceType.Computer),    name="deviceStatus"),
        ]
        systemItems = []
        for x in range(len(labels)):
            val = refs[x].get()
            if val.__str__() == 'Up':
                fieldContents = self._makeStatusRow(labelText=labels[x], statsRef=refs[x], fgColor=Theme.GREEN)
            else:
                fieldContents = self._makeStatusRow(labelText=labels[x], statsRef=refs[x], fgColor=Theme.RED)
            systemItems.append(fieldContents)

        systemsGridAttrs = {
            'bg_color':     Theme.BLACK,
            'border_color': Theme.LAMAS_MEDIUM_BLUE,
        }

        systemsGrid: Grid = Grid(systemItems, column_spacing=5, row_spacing=2, **systemsGridAttrs)
        return systemsGrid

    def _makeStatusRow(self, labelText: str, statsRef: AttrRef, formatStr: str = None, fgColor: tuple = None):

        labelAttrs = {
            'font':     self.statusFont,
            'bg_color': Theme.BLACK,
            'fg_color': Theme.WHITE,
        }
        fieldLabel: Label = Label(labelText, **labelAttrs)

        fieldAttrs = {
            'font':     self.statusFont,
            'bg_color': Theme.BLACK,
        }
        if fgColor is None:
            fieldAttrs['fg_color'] = Theme.WHITE
        else:
            fieldAttrs['fg_color'] = fgColor

        if formatStr is None:
            valueDisplay: DamageValueDisplay = DamageValueDisplay(ref=statsRef, **fieldAttrs)
        else:
            valueDisplay: DamageValueDisplay = ValueDisplay(ref=statsRef, format=formatStr, **fieldAttrs)

        fieldContent = [fieldLabel, valueDisplay]

        return fieldContent

    def _customizeConsoleContainer(self):

        pos = (self.settings.gameWidth + 2, 2)
        self.bg_color = Theme.BLACK
        self.fg_color = Theme.WHITE
        self.topleft = pos
        self.width   = 160 - 4
        self.height  = self.settings.gameHeight / 2
        self.margin  = 4
        self.border_width = 1
        self.border_color = Theme.GREEN
