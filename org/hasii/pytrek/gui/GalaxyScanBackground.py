
import pygame

from pygame import Surface

from org.hasii.pytrek.Settings import WHITE
from org.hasii.pytrek.Settings import RED
from org.hasii.pytrek.Settings import Settings

from org.hasii.pytrek.objects.Galaxy import Galaxy
from org.hasii.pytrek.objects.Coordinates import Coordinates

from org.hasii.pytrek.gui.gamepieces.GamePiece import GamePiece
from org.hasii.pytrek.gui.BaseBackground import BaseBackGround

from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.Intelligence import Intelligence

X_OFFSET    = 24
Y_OFFSET    = 16


class GalaxyScanBackground(BaseBackGround):
    """"""
    def __init__(self, screen: Surface):
        """"""

        super().__init__(screen, 'GalaxyScanBackground.png')

        self.computer = Computer()

        fqFileName: str = Settings.getResourcesPath(bareFileName=Settings.ALTERNATE_FIXED_WIDTH_FONT_NAME,
                                                    resourcePackageName=Settings.FONT_RESOURCES_PACKAGE_NAME,
                                                    resourcesPath=Settings.FONT_RESOURCES_PATH
                                                    )

        self.labelFont = pygame.font.Font(fqFileName, 14)

    def update(self, galaxy: Galaxy):
        """Displays galaxy content"""

        self.rect.x = 0
        self.rect.y = 0

        self.screen.blit(self.image, self.rect)

        for i in range(Intelligence.GALAXY_WIDTH):

            yPos = (i * GamePiece.QUADRANT_PIXEL_WIDTH) + X_OFFSET

            for j in range(Intelligence.GALAXY_HEIGHT):

                xPos = (j * GamePiece.QUADRANT_PIXEL_HEIGHT) + Y_OFFSET

                #
                # The galaxy was built in Column Major format
                #
                quadCoords = Coordinates(j, i)
                quadrant   = galaxy.getQuadrant(quadrantCoordinates=quadCoords)

                strValue = self.computer.createValueString(quadrant=quadrant)
                if quadrant.getCommanderCount() > 0:
                    label = self.labelFont.render(strValue, True, RED)
                else:
                    label    = self.labelFont.render(strValue, True, WHITE)
                self.screen.blit(label, (xPos, yPos))
