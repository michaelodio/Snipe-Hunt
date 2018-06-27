from nose.tools import *

import sys
sys.path.insert(0, '../projects')
from ETL import etl 

def test_display():
    vm = etl.VideoManager('../res/bunny.mp4')
    vm.display()
    vm.split()

def main():
    test_display
    
if __name__ == "__main__":
    main()