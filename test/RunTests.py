import unittest

import BaseTest
import ComputerTest
import CoordinateTest
import ExplosionColorTest
import GameEngineTest
import GameStatisticsTest
import QuadrantTest
import SettingsTest
import IntelligenceTest
import KlingonPowerTest


# Initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the suite
suite.addTest(loader.loadTestsFromModule(BaseTest))
suite.addTest(loader.loadTestsFromModule(ComputerTest))
suite.addTest(loader.loadTestsFromModule(CoordinateTest))
suite.addTest(loader.loadTestsFromModule(ExplosionColorTest))
suite.addTest(loader.loadTestsFromModule(GameEngineTest))
suite.addTest(loader.loadTestsFromModule(GameStatisticsTest))
suite.addTest(loader.loadTestsFromModule(IntelligenceTest))
suite.addTest(loader.loadTestsFromModule(KlingonPowerTest))
suite.addTest(loader.loadTestsFromModule(QuadrantTest))
suite.addTest(loader.loadTestsFromModule(SettingsTest))


# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print(result)