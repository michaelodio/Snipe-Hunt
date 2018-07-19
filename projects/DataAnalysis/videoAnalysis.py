import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

class videoAnalysis(object):

    def __init__(self): 
        self.conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")



def main():
    vidanalysis = videoAnalysis()
    print("created vidanalysis object\n")
   


if __name__ == "__main__":
    main()
    
