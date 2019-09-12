
from enum import Enum


class FutureEventType(Enum):

    FSPY        = 0   # spy event happens always (no future[] entry)
    FSNOVA      = 1   # Supernova
    FTBEAM      = 2   # Commander tractor beams Enterprise
    FSNAP       = 3   # Snapshot for time warp
    FBATTAK     = 4   # Commander attacks base
    FCDBAS      = 5   # Commander destroys base
    FSCMOVE     = 6   # Super Commander moves (might attack base)
    FSCDBAS     = 7   # Super Commander destroys base
    FDSPROB     = 8   # Move deep space probe

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
