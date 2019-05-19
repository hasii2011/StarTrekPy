import unittest

from unittest import TestCase
from org.hasii.pytrek.Settings import Settings

import os
class ConfigParserTest(TestCase):
    """More ha ha"""

    def setUp(self):
        """"""

    def testBasicSettings(self):
        """"""

        settings = Settings()

        self.assertEqual(2,settings.leftMargin)

        self.assertIsNotNone(settings.maxPlanets)
        self.assertIsNotNone(settings.maxStarCount)
        self.assertIsNotNone(settings.starBaseMaximum)
        self.assertIsNotNone(settings.starBaseMinimum)

        self.assertIsNotNone(settings.initialEnergyLevel)
        self.assertIsNotNone(settings.initialShieldEnergy)
        self.assertIsNotNone(settings.minimumImpulseEnergy)

        self.assertIsNotNone(settings.gameLengthFactor)
        self.assertIsNotNone(settings.starBaseExtender)
        self.assertIsNotNone(settings.starBaseMultiplier)

if __name__ == '__main__':
    unittest.main()