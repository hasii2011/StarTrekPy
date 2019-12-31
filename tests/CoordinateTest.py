import unittest
import logging

from tests.BaseTest import BaseTest
from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.engine.Direction import Direction

STANDARD_X_COORDINATE = 4
STANDARD_Y_COORDINATE = 4
EXPECTED_Y_COORDINATE_MOVEMENT_NORTH = 3
EXPECTED_Y_COORDINATE_MOVEMENT_SOUTH = 5
EXPECTED_X_COORDINATE_MOVEMENT_EAST  = 5
EXPECTED_X_COORDINATE_MOVEMENT_WEST  = 3

EXPECTED_X_COORDINATE_NE_MOVEMENT = 5
EXPECTED_Y_COORDINATE_NE_MOVEMENT = 3
EXPECTED_X_COORDINATE_NW_MOVEMENT = 3
EXPECTED_Y_COORDINATE_NW_MOVEMENT = 3
EXPECTED_X_COORDINATE_SW_MOVEMENT = 3
EXPECTED_Y_COORDINATE_SW_MOVEMENT = 5

EXPECTED_X_COORDINATE_SE_MOVEMENT = 5
EXPECTED_Y_COORDINATE_SE_MOVEMENT = 5


class CoordinateTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""

        self.logger = logging.getLogger(__name__)

    def testNewCoordinatesNorth(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.North)

        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_MOVEMENT_NORTH, "Should have decremented 'y'")

    def testNewCoordinatesSouth(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.South)

        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_MOVEMENT_SOUTH, "Should have incremented 'y'")

    def testNewCoordinatesEast(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.East)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_MOVEMENT_EAST, "Should have incremented 'x'")

    def testNewCoordinatesWest(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.West)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_MOVEMENT_WEST, "Should have decremented 'x'")

    def testNewCoordinatesNorthEast(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.NorthEast)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_NE_MOVEMENT, "Should have incremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_NE_MOVEMENT, "Should have decremented 'y'")

    def testNewCoordinatesNorthWest(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.NorthWest)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_NW_MOVEMENT, "Should have decremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_NW_MOVEMENT, "Should have decremented 'y'")

    def testNewCoordinatesSouthWest(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.SouthWest)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_SW_MOVEMENT, "Should have decremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_SW_MOVEMENT, "Should have incremented 'y'")

    def testNewCoordinatesSouthEast(self):
        coordinates   = Coordinates(STANDARD_X_COORDINATE, STANDARD_Y_COORDINATE)
        newCoordinate = coordinates.newCoordinates(Direction.SouthEast)

        self.assertEqual(newCoordinate.x, EXPECTED_X_COORDINATE_SE_MOVEMENT, "Should have incremented 'x'")
        self.assertEqual(newCoordinate.y, EXPECTED_Y_COORDINATE_SE_MOVEMENT, "Should have incremented 'y'")

    def testXTooSmall(self):
        coordinate = Coordinates(-1, 0)
        self.assertFalse(coordinate.valid())

    def testXTooBig(self):
        coordinate = Coordinates(10, 0)
        self.assertFalse(coordinate.valid())

    def testXLowBoundaryOk(self):
        coordinate = Coordinates(0, 0)
        self.assertTrue(coordinate.valid())

    def testXMidValueOk(self):
        coordinate = Coordinates(5, 0)
        self.assertTrue(coordinate.valid())

    def testXHighBoundaryOk(self):
        coordinate = Coordinates(9, 0)
        self.assertTrue(coordinate.valid())

    def testYTooSmall(self):
        coordinate = Coordinates(0, -1)
        self.assertFalse(coordinate.valid())

    def testYTooBig(self):
        coordinate = Coordinates(0, 10)
        self.assertFalse(coordinate.valid())

    def testYLowBoundaryOk(self):
        coordinate = Coordinates(0, 0)
        self.assertTrue(coordinate.valid())

    def testYMidValueOk(self):
        coordinate = Coordinates(0, 5)
        self.assertTrue(coordinate.valid())

    def testYHighBoundaryOk(self):
        coordinate = Coordinates(0, 9)
        self.assertTrue(coordinate.valid())


if __name__ == '__main__':
    unittest.main()
