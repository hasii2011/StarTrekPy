from enum import Enum


class PhaserStatus(Enum):
    """"""
    Down    = 0
    Up      = 1
    Damaged = 3

    def __str__(self):
        return str(self.name)

