import pygame

from org.hasii.pytrek.gui.GamePiece import GamePiece

class QuadrantBackground(GamePiece):
    """"""
    def __init__(self, screen: pygame.Surface):
        """"""
        super().__init__(screen=screen, fileNamePath='images/QuadrantBackground.png')
    def update(self):
        """Background always at 0,0"""

        self.rect.x = 0
        self.rect.y = 0

        self.screen.blit(self.image, self.rect)