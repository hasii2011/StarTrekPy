import unittest
import logging
import math

from unittest.mock import MagicMock
from pprint import pformat

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.objects.Quadrant import Quadrant

from org.hasii.pytrek.engine.Computer import Computer
from org.hasii.pytrek.engine.Direction import Direction
from org.hasii.pytrek.engine.KlingonPower import KlingonPower
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.Settings import Settings

from BaseTest import BaseTest

class ComputerTest(BaseTest):
    """ha ha"""

    MIN_QUADRANT_DISTANCE               = 0
    MAX_QUADRANT_DIAGONAL_DISTANCE      = 1.2
    MAX_QUADRANT_PERPENDICULAR_DISTANCE = 0.9
    MIN_GALACTIC_DISTANCE               = 0
    MAX_GALACTIC_DISTANCE               = 9.0
    N_RANDOM_DIRECTION_LOOPS            = 9
    N_RANDOM_POWER_LOOPS                = 5
    N_COMPUTE_HIT_VALUE_LOOPS           = 5
    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""

        self.logger       = logging.getLogger(__name__)

        self.settings     = Settings()
        self.computer     = Computer()

        mockCoordinates   = Coordinates(x=5, y=5)

        self.quadrant     = Quadrant(coordinates=mockCoordinates,screen=None)

    def testSingletonBehavior(self):

        doppleGanger = Computer()

        self.assertEqual(self.computer, doppleGanger, "Singleton creation failed")

        self.logger.info("computer: '%s',  doppleGanger: '%s'", self.computer.__repr__(), doppleGanger.__repr__())

    def testComputeQuadrantDistanceTopLeftToBottomRight(self):
        """"""

        startSectorCoordinates = Coordinates(Intelligence.MIN_SECTOR_X_COORDINATE,Intelligence.MIN_SECTOR_Y_COORDINATE)
        endSectorCoordinates   = Coordinates(Intelligence.MAX_SECTOR_X_COORDINATE,Intelligence.MAX_SECTOR_Y_COORDINATE)

        distance: float = self.computer.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)

        self.logger.info("Max distance is: %s", distance)
        self.assertGreater(distance, ComputerTest.MIN_QUADRANT_DISTANCE, "Max distance calculation failed less than zero")
        self.assertGreaterEqual(distance, ComputerTest.MAX_QUADRANT_DIAGONAL_DISTANCE, "Incorrect max distance")

    def testComputeQuadrantDistanceBottomRightToTopLeft(self):
        """"""

        startSectorCoordinates = Coordinates(Intelligence.MAX_SECTOR_X_COORDINATE,Intelligence.MAX_SECTOR_Y_COORDINATE)
        endSectorCoordinates   = Coordinates(Intelligence.MIN_SECTOR_X_COORDINATE,Intelligence.MIN_SECTOR_Y_COORDINATE)

        distance = self.computer.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)

        self.logger.info("Reverse Max distance is: %s", distance)
        self.assertGreater(distance, ComputerTest.MIN_QUADRANT_DISTANCE, "Max distance calculation failed less than zero")
        self.assertGreaterEqual(distance, ComputerTest.MAX_QUADRANT_DIAGONAL_DISTANCE, "Incorrect reverse max distance")

    def testComputeQuadrantDistanceEastToWest(self):
        """"""

        startSectorCoordinates = Coordinates(Intelligence.MIN_SECTOR_X_COORDINATE,Intelligence.MAX_SECTOR_Y_COORDINATE // 2)
        endSectorCoordinates   = Coordinates(Intelligence.MAX_SECTOR_X_COORDINATE,Intelligence.MAX_SECTOR_Y_COORDINATE // 2)

        self.logger.info("East to West coordinates %s, %s ", startSectorCoordinates, endSectorCoordinates)

        distance = self.computer.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)

        self.logger.info("East/West distance is: %s", distance)
        self.assertGreater(distance, ComputerTest.MIN_QUADRANT_DISTANCE, "East/West calculation failed less than zero")
        self.assertEqual(distance, ComputerTest.MAX_QUADRANT_PERPENDICULAR_DISTANCE, "Incorrect East/West distance")

    def testComputeQuadrantDistanceWestToEast(self):
        """"""
        startSectorCoordinates = Coordinates(Intelligence.MAX_SECTOR_X_COORDINATE,Intelligence.MAX_SECTOR_Y_COORDINATE // 2)
        endSectorCoordinates   = Coordinates(Intelligence.MIN_SECTOR_X_COORDINATE,Intelligence.MAX_SECTOR_Y_COORDINATE // 2)

        self.logger.info("Quadrant West to East sector coordinates %s, %s ", startSectorCoordinates, endSectorCoordinates)

        distance = self.computer.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)
        self.logger.info("West/East distance is: %s", distance)
        self.assertGreater(distance, ComputerTest.MIN_QUADRANT_DISTANCE, "East/West calculation failed less than zero")
        self.assertEqual(distance, ComputerTest.MAX_QUADRANT_PERPENDICULAR_DISTANCE, "Incorrect East/West distance")

    def testComputeQuadrantDistanceSmall(self):

        startSectorCoordinates = Coordinates(4,2)
        endSectorCoordinates   = Coordinates(4,8)

        self.logger.info("Small distance sector coordinates %s, %s ", startSectorCoordinates, endSectorCoordinates)
        distance = self.computer.computeQuadrantDistance(startSector=startSectorCoordinates, endSector=endSectorCoordinates)
        self.logger.info("West/East distance is: %s", distance)

    def testComputeGalacticDistanceWestToEast(self):
        """
        Not going to retest distance computations between inter-quadrant and galactic travel as galactic is just 10 times
        more expensive

        :return:
        """

        startQuadrantCoordinates = Coordinates(Intelligence.MAX_SECTOR_X_COORDINATE,math.floor(Intelligence.MAX_QUADRANT_Y_COORDINATE/2))
        endQuadrantCoordinates   = Coordinates(Intelligence.MIN_SECTOR_X_COORDINATE,math.floor(Intelligence.MAX_QUADRANT_Y_COORDINATE/2))

        self.logger.info("West to East quadrant coordinates %s, %s ", startQuadrantCoordinates, endQuadrantCoordinates)

        distance = self.computer.computeGalacticDistance(startQuadrantCoordinates=startQuadrantCoordinates, endQuadrantCoordinates=endQuadrantCoordinates)
        self.logger.info("Galactic West/East distance is: %s", distance)

        self.assertGreater(distance, ComputerTest.MIN_GALACTIC_DISTANCE, "East/West calculation failed less than zero")
        self.assertEqual(distance, ComputerTest.MAX_GALACTIC_DISTANCE, "Incorrect East/West distance")

    def testComputeSectorCoordinatesCenter(self):
        """"""

        xPos = (self.settings.gameWidth  / 2) - 1
        yPos = (self.settings.gameHeight / 2) - 1

        self.logger.info("Mouse click position; %s,%s", xPos,yPos)
        coordinates = self.computer.computeSectorCoordinates(xPos, yPos)

        self.assertIsNotNone(coordinates, "Where are my coordinates")
        self.logger.info("Sector %s", coordinates)

        self.assertEqual(coordinates.x, 4, "")
        self.assertEqual(coordinates.y, 4, "")

    def testComputeSectorCoordinatesExtremeRightLower(self):
        """"""

        xPos = self.settings.gameWidth  - 1
        yPos = self.settings.gameHeight - 1

        self.logger.info("Mouse click position; %s,%s", xPos,yPos)
        coordinates = self.computer.computeSectorCoordinates(xPos, yPos)

        self.assertIsNotNone(coordinates, "Where are my coordinates")
        self.logger.info("Sector %s", coordinates)

        self.assertEqual(coordinates.x, 9, "")
        self.assertEqual(coordinates.y, 9, "")

    def testComputeSectorCoordinatesExtremeLeftLower(self):
        """"""

        xPos = 0
        yPos = self.settings.gameHeight - 1

        self.logger.info("Mouse click position; %s,%s", xPos,yPos)
        coordinates = self.computer.computeSectorCoordinates(xPos, yPos)

        self.assertIsNotNone(coordinates, "Where are my coordinates")
        self.logger.info("Sector %s", coordinates)

        self.assertEqual(coordinates.x, 0, "")
        self.assertEqual(coordinates.y, 9, "")

    def testComputeSectorCoordinatesExtremeRightUpper(self):
        """"""

        xPos = self.settings.gameWidth  - 1
        yPos = 1

        self.logger.info("Mouse click position; %s,%s", xPos,yPos)
        coordinates = self.computer.computeSectorCoordinates(xPos, yPos)

        self.assertIsNotNone(coordinates, "Where are my coordinates")
        self.logger.info("Sector %s", coordinates)

        self.assertEqual(coordinates.x, 9, "Wrong y coordinate")
        self.assertEqual(coordinates.y, 0, "Wrong y coordinate")

    def testValueStringEmptyQuadrant(self):
        """"""

        self.quadrant.klingonCount = 0
        self.quadrant.starBase     = False

        strValue = self.computer.createValueString(self.quadrant)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("000", strValue, "Empty quadrant is all zeroes")

    def testValueStringMultiKlingon(self):
        """"""

        self.quadrant.klingonCount = 0
        self.quadrant.starBase     = False
        self.quadrant.addKlingon()
        self.quadrant.addKlingon()
        self.quadrant.addKlingon()

        strValue = self.computer.createValueString(self.quadrant)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("300", strValue, "Must contain 3 Klingons and no starbase")

    def testValueStringMultiKlingonAndStarbase(self):
        """"""

        self.quadrant.klingonCount = 0
        self.quadrant.starBase     = True
        self.quadrant.addKlingon()
        self.quadrant.addKlingon()
        self.quadrant.addKlingon()
        self.quadrant.addKlingon()

        strValue = self.computer.createValueString(self.quadrant)

        self.assertIsNotNone(strValue, "Where is my string")
        self.assertEqual("410", strValue, "Must contain 4 Klingons and a starbase")

    def testDoStraightLineInterpolationExtremeWestDown(self):
        """"""

       # [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)]
        expectedCoordinates = [Coordinates(0,1), Coordinates(0,2), Coordinates(0,3), Coordinates(0,4),
                               Coordinates(0,5), Coordinates(0,6), Coordinates(0,7), Coordinates(0,8),
                               Coordinates(0,9)
                               ]
        x0 = 0
        y0 = 0
        y1 = 9

        interceptCoordinates = self.computer.doStraightLineInterpolation(x0, y0, y1)

        self.assertIsNotNone(interceptCoordinates, "Better return some  thing")
        self.assertEqual(9, len(interceptCoordinates), "Should have maximum coordinates")

        self.logger.info("interceptCoordinates: %s", pformat(interceptCoordinates))
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testDoStraightLineInterpolationExtremeWestUp(self):
        """"""

       # [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0,9)]
        expectedCoordinates = [Coordinates(0,8), Coordinates(0,7), Coordinates(0,6), Coordinates(0,5),
                               Coordinates(0,4), Coordinates(0,3), Coordinates(0,2), Coordinates(0,1),
                               Coordinates(0,0)
                               ]
        x0 = 0
        y0 = 9
        y1 = 0

        interceptCoordinates = self.computer.doStraightLineInterpolation(x0, y0, y1)

        self.assertIsNotNone(interceptCoordinates, "Better return some  thing")
        self.assertEqual(9, len(interceptCoordinates), "Should have maximum coordinates")

        self.logger.info("interceptCoordinates: %s", pformat(interceptCoordinates))
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testDoStraightLineInterpolationExtremeEastDown(self):
        """"""

        # [(9,9),(9,8), (9,7), (9,6), (9,5), (9,4), (9,3), (9,2), (9,1)]
        expectedCoordinates = [Coordinates(9, 1), Coordinates(9, 2), Coordinates(9, 3), Coordinates(9, 4),
                               Coordinates(9, 5), Coordinates(9, 6), Coordinates(9, 7), Coordinates(9, 8),
                               Coordinates(9,9)
                               ]
        x0 = 9
        y0 = 0
        y1 = 9

        interceptCoordinates = self.computer.doStraightLineInterpolation(x0, y0, y1)

        self.assertIsNotNone(interceptCoordinates, "Better return some thing")
        self.assertEqual(9, len(interceptCoordinates), "Should have maximum coordinates")
        self.logger.info("interceptCoordinates: %s", pformat(interceptCoordinates))
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testDoStraightLineInterpolationExtremeEastUp(self):
        """"""

        # [(0,8), (0,7), (0,6), (0,5), (0,4), (0,3), (0,2), (0,1), (0,0)]
        expectedCoordinates = [Coordinates(0, 8), Coordinates(0, 7), Coordinates(0, 6), Coordinates(0, 5),
                               Coordinates(0, 4), Coordinates(0, 3), Coordinates(0, 2), Coordinates(0, 1),
                               Coordinates(0,0)
                               ]
        x0 = 0
        y0 = 9
        y1 = 0
        interceptCoordinates = self.computer.doStraightLineInterpolation(x0, y0, y1)
        self.assertIsNotNone(interceptCoordinates, "Better return some thing")
        self.assertEqual(9, len(interceptCoordinates), "Should have maximum coordinates")
        self.logger.info("interceptCoordinates: %s", pformat(interceptCoordinates))
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testInterpolateYInterceptsDoStraightLine(self):
        """"""

        expectedCoordinates = [Coordinates(0, 1), Coordinates(0, 2), Coordinates(0, 3), Coordinates(0, 4),
                               Coordinates(0, 5), Coordinates(0, 6), Coordinates(0, 7), Coordinates(0, 8)
                               ]

        mockComputer = Computer()
        mockComputer.doStraightLineInterpolation = MagicMock(return_value = expectedCoordinates)

        start: Coordinates = Coordinates(0,0)
        end:   Coordinates = Coordinates(0,9)
        interceptCoordinates = mockComputer.interpolateYIntercepts(start=start, end=end)

        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testInterpolateYInterceptsDoDiagonalNWtoSE(self):
        """"""

        expectedCoordinates = [Coordinates(1, 1), Coordinates(2, 2), Coordinates(3, 3), Coordinates(4, 4),
                               Coordinates(5, 5), Coordinates(6, 6), Coordinates(7, 7), Coordinates(8, 8),
                               Coordinates(9,9)
                               ]

        start: Coordinates = Coordinates(0,0)
        end:   Coordinates = Coordinates(9,9)

        interceptCoordinates = self.computer.interpolateYIntercepts(start=start, end=end)
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testInterpolateYInterceptsDoDiagonalNEtoSW(self):
        """"""

        expectedCoordinates = [Coordinates(1, 8), Coordinates(2, 7), Coordinates(3, 6), Coordinates(4, 5),
                               Coordinates(5, 4), Coordinates(6, 3), Coordinates(7, 2), Coordinates(8, 1),
                               Coordinates(9,0)
                               ]

        start: Coordinates = Coordinates(0,9)
        end:   Coordinates = Coordinates(9,0)

        interceptCoordinates = self.computer.interpolateYIntercepts(start=start, end=end)
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Computed coordinates did not match")

    def testInterpolateYInterceptsOddTest(self):
        """"""

        # I think this is a bug
        expectedCoordinates = [Coordinates(4,4), Coordinates(4,4)]

        start: Coordinates = Coordinates(5,0)
        end:   Coordinates = Coordinates(4,4)

        interceptCoordinates = self.computer.interpolateYIntercepts(start=start, end=end)
        self.assertListEqual(expectedCoordinates, interceptCoordinates, "Odd test found bug")

    def testDetermineDirectionNorth(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(4,0)

        expectedDirection: Direction = Direction.North
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionSouth(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(4,9)

        expectedDirection: Direction = Direction.South
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionEast(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(9,4)

        expectedDirection: Direction = Direction.East
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionWest(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(0,4)

        expectedDirection: Direction = Direction.West
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionNorthEast(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(9,0)

        expectedDirection: Direction = Direction.NorthEast
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionNorthWest(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(0,0)

        expectedDirection: Direction = Direction.NorthWest
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionSouthWest(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(0,9)

        expectedDirection: Direction = Direction.SouthWest
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testDetermineDirectionSouthEast(self):
        """"""

        startCoordinates: Coordinates = Coordinates(4,4)
        endCoordinates:   Coordinates = Coordinates(9,9)

        expectedDirection: Direction = Direction.SouthEast
        actualDirection:   Direction = self.computer.determineDirection(startCoordinates=startCoordinates, endCoordinates=endCoordinates)

        self.assertEqual(expectedDirection, actualDirection, "Computer appears to have a bug")

    def testRandomDirection(self):
        """"""

        for x in range(0, ComputerTest.N_RANDOM_DIRECTION_LOOPS):

            direction = self.computer.randomDirection()
            self.assertIsNotNone(direction, "Should at least return a direction"
                                            "")
            self.logger.info("Random direction name: '%s', value: '%s'", direction.name,direction.value)

    def test_ComputeCourseZeroZeroToNineNine(self):

        klingonCoordinates:    Coordinates = Coordinates(0,0)
        enterpriseCoordinates: Coordinates = Coordinates(9,9)

        course: float = self.computer._computeCourse(start=klingonCoordinates, end=enterpriseCoordinates)
        self.assertIsNotNone(course, "Should return a course")
        self.assertAlmostEqual(course, 4.4999, 3)
        self.logger.info("Course ZeroZeroToNineNine: '%s'", course)

    def test_ComputeCourseNineNineToZeroZero(self):

        klingonCoordinates:    Coordinates = Coordinates(9,9)
        enterpriseCoordinates: Coordinates = Coordinates(0,0)

        course: float = self.computer._computeCourse(start=klingonCoordinates, end=enterpriseCoordinates)
        self.assertIsNotNone(course, "Should return a course")
        self.assertAlmostEqual(course, -1.4999, 3)
        self.logger.info("Course NineNineToZeroZero: '%s'", course)

    def test_ComputeCourseNineZeroToZeroNine(self):

        klingonCoordinates:    Coordinates = Coordinates(9,0)
        enterpriseCoordinates: Coordinates = Coordinates(0,9)

        course: float = self.computer._computeCourse(start=klingonCoordinates, end=enterpriseCoordinates)
        self.assertIsNotNone(course, "Should return a course")
        self.assertAlmostEqual(course, 1.4999, 3)
        self.logger.info("Course NineZeroToZeroNine: '%s'", course)

    def test_ComputeCourseFourZeroToFourNine(self):

        klingonCoordinates:    Coordinates = Coordinates(4,0)
        enterpriseCoordinates: Coordinates = Coordinates(4,9)

        course: float = self.computer._computeCourse(start=klingonCoordinates, end=enterpriseCoordinates)
        self.assertIsNotNone(course, "Should return a course")
        self.assertAlmostEqual(course, 2.9999, 3)
        self.logger.info("Course FourZeroToFourNine: '%s'", course)

    def test_ComputeCourseFourNineToFourZero(self):

        klingonCoordinates:    Coordinates = Coordinates(4,9)
        enterpriseCoordinates: Coordinates = Coordinates(4,0)

        course: float = self.computer._computeCourse(start=klingonCoordinates, end=enterpriseCoordinates)
        self.assertIsNotNone(course, "Should return a course")
        self.assertAlmostEqual(course, -2.9999, 3)
        self.logger.info("Course FourNineToFourZero: '%s'", course)

    def test_RandomizeAttackerPower(self):

        for x in range(0, ComputerTest.N_RANDOM_POWER_LOOPS):
            randomPower = self.computer._randomizeAttackerPower(KlingonPower.Fair.value)

            self.assertIsNotNone(randomPower, "Should generate some value.")
            self.assertGreater(randomPower, 0, "Should always be greater than zero")
            self.logger.info("Test %s, randomPower: '%s'", x, randomPower)

    def testComputeHitValueOnEnterpriseFarAwayEmeritus(self):

        klingonCoordinates:    Coordinates = Coordinates(0,0)
        enterpriseCoordinates: Coordinates = Coordinates(9,9)
        klingonPower:          float       = KlingonPower.Emeritus.value

        hitValue: float = self.computer.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info("Emeritus Far away.  Klingon hit value: %s", hitValue)

    def testComputeHitValueOnEnterpriseUpCloseEmeritus(self):

        klingonCoordinates:    Coordinates = Coordinates(4,4)
        enterpriseCoordinates: Coordinates = Coordinates(4,5)
        klingonPower:          float       = KlingonPower.Emeritus.value

        hitValue: float = self.computer.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info("Emeritus Up Close.  Klingon hit value: %s", hitValue)

    def testComputeHitValueOnEnterpriseFarAwayNovice(self):

        klingonCoordinates:    Coordinates = Coordinates(0,0)
        enterpriseCoordinates: Coordinates = Coordinates(9,9)
        klingonPower:          float       = KlingonPower.Novice.value

        hitValue: float = self.computer.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info("Novice Far away.  Klingon hit value: %s", hitValue)

    def testComputeHitValueOnEnterpriseUpCloseNovice(self):

        klingonCoordinates:    Coordinates = Coordinates(4,5)
        enterpriseCoordinates: Coordinates = Coordinates(4,4)
        klingonPower:          float       = KlingonPower.Novice.value

        hitValue: float = self.computer.computeHitValueOnEnterprise(klingonCoordinates, enterpriseCoordinates, klingonPower)
        self.logger.info("Novice Up Close.  Klingon hit value: %s", hitValue)

    def testModulusOnDirection(self):

        modNorth     = Direction.North.value % 90
        modSouth     = Direction.South.value % 90
        modNorthWest = Direction.NorthWest.value % 90
        modSouthEast = Direction.SouthEast.value % 90

        self.logger.info("modNorth: '%s' modSouth: '%s' modNorthWest: '%s' modSouthEast: '%s'", modNorth, modSouth, modNorthWest, modSouthEast)
if __name__ == '__main__':
    unittest.main()