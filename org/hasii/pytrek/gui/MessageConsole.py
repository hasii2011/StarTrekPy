
from pygame.font import Font

from albow.themes.Theme import Theme

from albow.widgets.TextBox import TextBox

from org.hasii.pytrek.Settings import Settings


class MessageConsole(TextBox):

    def __init__(self):

        super().__init__(theNumberOfRows=10, theNumberOfColumns=53)

        messageFont: Font     = Font("fonts/MonoFonto.ttf", 14)
        settings:    Settings = Settings()

        pos = (4, settings.gameHeight)

        self.bg_color = Theme.BLACK
        self.fg_color = Theme.WHITE
        self.font     = messageFont
        self.topleft = pos
