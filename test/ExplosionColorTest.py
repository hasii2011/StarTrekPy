
import unittest
import logging

from BaseTest import BaseTest
from org.hasii.pytrek.gui.ExplosionColor import ExplosionColor

class ExplosionColorTest(BaseTest):
    """ha ha"""

    @classmethod
    def setUpClass(cls):
        """"""
        print("__name__ : " + __name__)
        BaseTest.setUpLogging()

    def setUp(self):
        """"""
        self.logger       = logging.getLogger(__name__)

    def testSuccessorFromUnknown(self):
        """"""
        color:     ExplosionColor = ExplosionColor.NO_COLOR
        nextColor: ExplosionColor = color.successor()

        self.assertEqual(nextColor, ExplosionColor.GREY, "Successor from unknown does not work")

    def testSuccessorFromBlue(self):
        """"""
        color:     ExplosionColor = ExplosionColor.BLUE
        nextColor: ExplosionColor = color.successor()

        self.assertEqual(nextColor, ExplosionColor.RED, "Successor from Blue does not work")

    def testWrapAroundFromBottom(self):
        """"""
        color:     ExplosionColor = ExplosionColor.WHITE
        nextColor: ExplosionColor = color.successor()

        self.assertEqual(nextColor, ExplosionColor.NO_COLOR, "Wrap around from last color did not work")


    def testPredecessorFromBlue(self):
        """"""
        color:     ExplosionColor = ExplosionColor.BLUE
        nextColor: ExplosionColor = color.predecessor()

        self.assertEqual(nextColor, ExplosionColor.GREY, "Predecessor from Blue does not work")

    def testPredecessorFromBottom(self):
        """"""
        color:     ExplosionColor = ExplosionColor.WHITE
        nextColor: ExplosionColor = color.predecessor()

        self.assertEqual(nextColor, ExplosionColor.RED, "Predecessor from bottom does not work")

    def testPredecessorFromTop(self):
        """"""

        color:     ExplosionColor = ExplosionColor.NO_COLOR
        nextColor: ExplosionColor = color.predecessor()

        self.assertEqual(nextColor, ExplosionColor.WHITE, "Predecessor from top does not work")




if __name__ == '__main__':
    unittest.main()