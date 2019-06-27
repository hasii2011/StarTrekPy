from enum import Enum


class ShieldStatus(Enum):
    """Describes the possible shield status's"""
    Down    = 0
    Up      = 1
    Damaged = 3

    def __str__(self):
        return str(self.name)
