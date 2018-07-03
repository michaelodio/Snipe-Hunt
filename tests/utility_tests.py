
import sys
sys.path.insert(0, '../projects/ETL/')
from Utility import *


def test_get_file_paths():
    """ Tests the get_file_paths method """
    util = Utility()
    util.get_file_paths("../res/")


def test_display_file_paths():
    """ Tests the display_file method """
    util = Utility()
    util.get_file_paths("../res/")
    util.display_file_paths()


def test():
    """ Runs all test methods for this class """
    test_get_file_paths()
    test_display_file_paths()
    print "    Utility: Passed"


if __name__ == "__main__":
    test()
