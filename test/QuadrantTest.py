import unittest
import logging

from BaseTest import BaseTest

from org.hasii.pytrek.objects.Coordinates import Coordinates
from org.hasii.pytrek.engine.Intelligence import Intelligence
from org.hasii.pytrek.objects.Quadrant import Quadrant
from org.hasii.pytrek.objects.SectorType import SectorType


class QuadrantTest(BaseTest):
    """ha ha"""

    @classmethod
    def setUpClass(cls):
        """"""
        BaseTest.setUpLogging()

    def setUp(self):
        """"""

        self.intelligence = Intelligence()
        self.logger       = logging.getLogger(__name__)

        mockCoordinates   = Coordinates(x=5, y=5)
        self.quadrant     = Quadrant(coordinates=mockCoordinates, screen=None);

    def testGetRandomEmptySector(self):
        """"""

        sector = self.quadrant.getRandomEmptySector()

        self.assertIsNotNone(sector, "Gotta get a sector back")
        self.assertEqual(sector.sectorType, SectorType.EMPTY, "sector should be empty")

        self.logger.info("retrieved sector: %s", sector)

    def testSetKlingons(self):
        """"""

        self.quadrant.addKlingon()
        self.quadrant.addKlingon()

        actualKlingonCount = self.quadrant.getKlingonCount()

        self.assertEqual(2, actualKlingonCount, "mismatched Klingon Count")

        klingons = self.quadrant.klingons

        actualKlingonObjects = klingons.__len__()

        self.assertEqual(2, actualKlingonObjects, "mismatched Klingon object created")


if __name__ == '__main__':
    unittest.main()
