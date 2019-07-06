
from logging import Logger
from logging import getLogger

from org.hasii.pytrek.objects.Coordinates import Coordinates

from org.hasii.pytrek.engine.futures.FutureEventType import FutureEventType


class FutureEvent:

    def __init__(self, fEventType: FutureEventType, starDate: float = 0.0, qCoordinates: Coordinates = None):

        self.logger: Logger = getLogger(__name__)

        self._eventType:    FutureEventType = fEventType
        self._starDate:     float           = starDate
        self._qCoordinates: Coordinates     = qCoordinates

    def getEventType(self) -> FutureEventType:
        return self._eventType

    def setEventType(self, theNewValue: FutureEventType):
        self._eventType = theNewValue

    def getStarDate(self) -> float:
        return self._starDate

    def setStarDate(self, theNewValue: float):
        self._starDate = theNewValue

    def getQCoordinates(self) -> Coordinates:
        return self._qCoordinates

    def setQCoordinates(self, theNewValue: Coordinates):
        self._qCoordinates = theNewValue

    eventType    = property(getEventType, setEventType)
    starDate     = property(getStarDate, setStarDate)
    qCoordinates = property(getQCoordinates, setQCoordinates)

    def __repr__(self):

        representation = (
            f"eventType: {self.eventType:8} "
            f"starDate: {self.starDate:5.2f} "
            f"qCoordinates: '{self.qCoordinates}'"
        )
        return representation
