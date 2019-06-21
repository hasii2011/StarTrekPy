import logging

import os
import pygame
from pygame.sprite import Sprite

from org.hasii.pytrek.Settings import WHITE
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.gui.GamePiece import GamePiece

Y_OFFSET           = 2
LABEL_X            = 2
INITIAL_MESSAGE_Y  = Intelligence.GALAXY_HEIGHT * GamePiece.QUADRANT_PIXEL_HEIGHT + Y_OFFSET

MESSAGE_X          = LABEL_X + 16
MESSAGE1_Y         = INITIAL_MESSAGE_Y
MESSAGE2_Y         = MESSAGE1_Y + 16
MESSAGE3_Y         = MESSAGE2_Y + 16

FONT_PATH          = "fonts/MonoFonto.ttf"

UPDATE_INTERVAL_SECONDS = 1


class MessageWindow(Sprite):
    """

    """
    def __init__(self, screen: pygame.Surface):
        """"""

        super().__init__()

        self.screen = screen
        self.logger = logging.getLogger(__name__)

        self.messageFont    = pygame.font.Font(FONT_PATH, 14)

        self.messageStrings = ["Message 1", "Message 2", "Message 3"]
        self.messages       = ["", "", ""]
        self.messageY       = [MESSAGE1_Y, MESSAGE2_Y, MESSAGE3_Y]

        fileName            = os.path.join('sounds', 'tos_com_beep_2.wav')
        self.beep           = pygame.mixer.Sound(fileName)

    def update(self):
        """"""

        for x in range(len(self.messageStrings)):
            self.messages[x] = self.messageFont.render(self.messageStrings[x], 1, WHITE)
            self.screen.blit(self.messages[x], (MESSAGE_X, self.messageY[x]))

    def displayMessage(self, newMessage: str, makeSound: bool = False):
        """"""

        self.messageStrings[2] = self.messageStrings[1]
        self.messageStrings[1] = self.messageStrings[0]
        self.messageStrings[0] = newMessage
        if makeSound is True:
            self.beep.play()
        else:
            self.logger.debug("No beep")
