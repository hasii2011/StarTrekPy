
from typing import Tuple

from pygame import Surface

from albow.widgets.ValueDisplay import ValueDisplay
from albow.themes.Theme import Theme

from org.hasii.pytrek.engine.ShipCondition import ShipCondition


class ShipConditionValueDisplay(ValueDisplay):

    YELLOW:     Tuple[int, int, int] = (255, 255, 0)      # Until Albow has this color
    LIGHT_BLUE: Tuple[int, int, int] = (153, 204, 255)    # Until Albow has this color

    def __init__(self, **kwds):

        super().__init__(**kwds)

    def draw(self, surface: Surface):

        if isinstance(self.value, ShipCondition):
            if self.value == ShipCondition.Green:
                self.fg_color = Theme.GREEN
            elif self.value == ShipCondition.Red:
                self.fg_color = Theme.RED
            elif self.value == ShipCondition.Yellow:
                self.fg_color = ShipConditionValueDisplay.YELLOW
            elif self.value == ShipCondition.Docked:
                self.fg_color = ShipConditionValueDisplay.LIGHT_BLUE
            else:
                # dead, dead, dead !!
                self.fg_color = Theme.LAMAS_OFF_WHITE

        super().draw(surface)
