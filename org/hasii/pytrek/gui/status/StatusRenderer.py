
import pygame

from pygame.font import Font
from pygame import Surface

from org.hasii.pytrek.Settings import WHITE
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.gui.GamePiece import GamePiece

X_OFFSET       = 10
LABEL_X        = Intelligence.GALAXY_WIDTH * GamePiece.QUADRANT_PIXEL_WIDTH + X_OFFSET
VALUE_OFFSET_X = LABEL_X + 85

FONT_PATH      = "fonts/MonoFonto.ttf"

class StatusRenderer:
    """
        Display's a particular value as a label and value
        Private component for status console

    """
    def __init__(self, screen: Surface, label: str, yPos: int):
        """"""

        self.screen:      Surface = screen
        self.textFont:    Font    =  pygame.font.Font(FONT_PATH, 14)
        self.statusLabel: Surface = self.textFont.render(label, 1, WHITE)
        self.labelXY:     tuple   = (LABEL_X, yPos)
        self.labelXY:     tuple   = (LABEL_X, yPos)
        self.valueXY:     tuple   = (VALUE_OFFSET_X, yPos)

    def display(self, newValue, color):
        """"""

        displayableValue: Surface    = self.textFont.render(newValue, 1, color)

        self.screen.blit(self.statusLabel, (self.labelXY[0], self.labelXY[1]))
        self.screen.blit(displayableValue, (self.valueXY[0], self.valueXY[1]))

