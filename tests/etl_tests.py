from nose.tools import *

import sys
sys.path.insert(0, '../projects/ETL/')
from etl import * 


def test_display():
    """ Tests the display method of etl """
    vm = VideoManager('../res/bunny.mp4')
    vm.display()
    #vm.split()


def main():
    """ Auto run main method """
    test_display()


if __name__ == "__main__":
    main()
