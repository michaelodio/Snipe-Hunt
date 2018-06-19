from nose.tools import *

import sys
sys.path.insert(0, 'C:\\Users\\Matt\\Desktop\\Python\\French-Flag-Finder\\projects\\ETL\\')
from ETL import etl 

def test_display():
    vm = etl.VideoManager('C:\\Users\\Matt\\Desktop\\Python\\French-Flag-Finder\\projects\\ETL\\res\\bunny.mp4')
    vm.display()
    vm.split()

def main():
    test_display
    
if __name__ == "__main__":
    main()