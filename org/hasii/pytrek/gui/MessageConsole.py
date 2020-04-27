from pkg_resources import resource_filename
from pygame.font import Font

from albow.themes.Theme import Theme

from albow.widgets.TextBox import TextBox

from org.hasii.pytrek.Settings import Settings


class MessageConsole(TextBox):

    CONSOLE_FONT_SIZE: int = 14

    def __init__(self):

        super().__init__(theNumberOfRows=10, theNumberOfColumns=53)

        fqFileName = resource_filename(Settings.FONT_RESOURCES_PACKAGE_NAME, Settings.FIXED_WIDTH_FONT_NAME)

        messageFont: Font     = Font(fqFileName, MessageConsole.CONSOLE_FONT_SIZE)
        settings:    Settings = Settings()

        pos = (4, settings.gameHeight)

        self.bg_color = Theme.BLACK
        self.fg_color = Theme.WHITE
        self.font     = messageFont
        self.topleft = pos
