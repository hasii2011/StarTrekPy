
from enum import Enum


class ExplosionColor(Enum):

    NO_COLOR = 1
    GREY     = 2
    BLUE     = 4
    RED      = 8
    WHITE    = 16

    def successor(self):
        v = self.value * 2
        if v > 16:
            return ExplosionColor.NO_COLOR
        return ExplosionColor(v)

    def predecessor(self):
        v = self.value // 2
        if v == 0:
            return ExplosionColor.WHITE
        return ExplosionColor(v)

    __order__ = 'NO_COLOR GREY BLUE RED WHITE'
