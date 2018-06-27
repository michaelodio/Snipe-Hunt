from nose.tools import *

import sys
sys.path.insert(0, 'C:\\Users\\Matt\\Desktop\\Python\\French-Flag-Finder\\projects\\ETL\\')
from ETL import utility 


def test_get_file_paths():
    util = Utility()
    util.get_file_paths("C:\Users\micha\OneDrive\Desktop\movies")

def test_display_file_paths():
    print("something")