import unittest


from ComputerTest import ComputerTest
from CoordinateTest import CoordinateTest
from ExplosionColorTest import ExplosionColorTest
from GameEngineTest import GameEngineTest
from GameStatisticsTest import GameStatisticsTest
from QuadrantTest import QuadrantTest
from SettingsTest import SettingsTest
from IntelligenceTest import IntelligenceTest
from KlingonPowerTest import KlingonPowerTest

#
# Because of the way the unit test debug logging is set up the test runner needs to run
# from the project working directory
#
# Initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the suite
suite.addTest(loader.loadTestsFromTestCase(ComputerTest))
suite.addTest(loader.loadTestsFromTestCase(CoordinateTest))
suite.addTest(loader.loadTestsFromTestCase(ExplosionColorTest))
suite.addTest(loader.loadTestsFromTestCase(GameEngineTest))
suite.addTest(loader.loadTestsFromTestCase(GameStatisticsTest))
suite.addTest(loader.loadTestsFromTestCase(IntelligenceTest))
suite.addTest(loader.loadTestsFromTestCase(KlingonPowerTest))
suite.addTest(loader.loadTestsFromTestCase(QuadrantTest))
suite.addTest(loader.loadTestsFromTestCase(SettingsTest))


# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

print(f"THE RESULTS ARE IN\n{result}")
