
import sys
sys.path.insert(0, '../projects/ETL/')
from etl import *


def test_display():
    """ Tests the display method of etl """
    vm = VideoManager('../res/bunny.mp4')
    vm.display()
    #vm.split()


def test():
    """ Runs all test methods for this class """
    test_display()
    print "    ETL: Passed"


if __name__ == "__main__":
    test()
