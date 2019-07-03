
from pygame import Surface

from albow.widgets.ValueDisplay import ValueDisplay
from albow.themes.Theme import Theme

from org.hasii.pytrek.engine.DeviceStatus import DeviceStatus


class DamageValueDisplay(ValueDisplay):

    def __init__(self, **kwds):

        super().__init__(**kwds)

    def draw(self, surface: Surface):

        if isinstance(self.value, DeviceStatus):
            if self.value == DeviceStatus.Up:
                self.fg_color = Theme.GREEN
            else:
                self.fg_color = Theme.RED
        super().draw(surface)
