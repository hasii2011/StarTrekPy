
from enum import Enum


class FutureEventType(Enum):

    FSNOVA      = 1   # Supernova
    FTBEAM      = 2   # Commander tractor beams Enterprise
    FSNAP       = 3   # Snapshot for time warp
    FBATTAK     = 4   # Commander attacks base
    FCDBAS      = 5   # Commander destroys base
    FSCMOVE     = 6   # Super Commander moves (might attack base)
    FSCDBAS     = 7   # Super Commander destroys base
    FDSPROB     = 8   # Move deep space probe
    FDISTR      = 9   # Emit distress call from an inhabited world
    FENSLV      = 10  # Inhabited word is enslaved */
    FREPRO      = 11  # Klingons build a ship in an enslaved system
    FCMOREPOWER = 12  # Commander regains power if it is far enough away from our ship
