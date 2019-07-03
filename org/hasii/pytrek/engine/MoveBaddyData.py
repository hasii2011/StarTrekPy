from dataclasses import dataclass

from org.hasii.pytrek.engine.PlayerType import PlayerType


@dataclass
class MoveBaddyData:

    playerSkill:             PlayerType
    numberOfKlingons:        int
    numberOfCommanders:      int
    numberOfSuperCommanders: int = 0
    numberOfRomulans:        int = 0

