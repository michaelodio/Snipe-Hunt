import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

class videoAnalysis(object):

    def __init__(self): 
        self.logger = Utilities.setup_logger("videoanalysis", '../../logs/videoAnalysis.log')
        self.count = 0
        self.totalFrames = None
        self.averageTargetConfidence = 0.0
        self.conn = None
        self.targetConfidenceHi = 0.0
        self.targetConfidenceLo = 100.0
        self.targetConfidenceHiFrame = None
        self.targetConfidenceLoFrame = None
        self.generalObjectsFound = set()


    def readyForAnalysis(self, table):
        self.logger.info("Checking if a video is ready for analysis...")
        self.logger.info("Attempting to connect to Accumulo...")
        try:
            self.conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")
        except:
            self.logger.info("Failed to connect to Accumulo")
            raise ValueError("Failed to make connection to accumulo!\n") 
        self.logger.info("established connection successfully")
        try:
            for entry in self.conn.scan(table):
                if self.count == 0:
                    self.totalFrames = json.loads(entry.val)['videoMetadata']['totalFrames']
                self.count = self.count + 1
                print(self.count)   #only used for testing/debugging
        except:
            self.logger.info("Failed to scan table in Accumulo! Shutting down conn")
            raise ValueError("Failed to scan table in Accumulo! Shutting down conn")
            self.conn.close()
        self.logger.info("number of entries = " + str(self.count))
        self.logger.info("Total frames = " + str(self.totalFrames))
        if self.count == self.totalFrames:
            self.logger.info("Video is ready for analysis!")
            return True
        self.logger.info("Video is not ready for analysis!")
        return False
        
        
    def calculateAverageTargetConfidence(self, table):
        self.logger.info("Calculating the average target confidence across the whole video...")
        try:
            for entry in self.conn.scan(table):
                json_data_parsed = json.loads(entry.val)
                if 'foundTargetWithConfidence' in json_data_parsed['frameMetadata']:
                    percent = float(json_data_parsed['frameMetadata']['foundTargetWithConfidence'])
                    self.averageTargetConfidence = self.averageTargetConfidence + percent
                    if percent < self.targetConfidenceLo:
                        self.targetConfidenceLo = percent
                        self.targetConfidenceLoFrame = int(json_data_parsed['frameMetadata']['frameNum'])
                    if percent > self.targetConfidenceHi:
                        self.targetConfidenceHi = percent
                        self.targetConfidenceHiFrame = int(json_data_parsed['frameMetadata']['frameNum'])
        except:
            self.logger.info("Failed to scan table in Accumulo! Shutting down conn")
            raise ValueError("Failed to scan table in Accumulo! Shutting down conn")
            self.conn.close()
        self.averageTargetConfidence = self.averageTargetConfidence / self.totalFrames  #divides by total frames to calculate avg target confidence across whole video
        print("Final data:\n")
        self.logger.info("The average target confidence across the whole video = " + str(self.averageTargetConfidence))
        self.logger.info("The highest target confidence across the whole video = " + str(self.targetConfidenceHi))
        self.logger.info("The highest target confidence frame num = " + str(self.targetConfidenceHiFrame))
        self.logger.info("The lowest target confidence across the whole video = " + str(self.targetConfidenceLo))
        self.logger.info("The lowest target confidence frame num = " + str(self.targetConfidenceLoFrame))
        self.conn.close()    
        
        
    def AverageGenObjectConfidence(self, table):
        self.logger.info("Calculating the average gen obj confidence across the whole video...")
        try:
            for entry in self.conn.scan(table):
                json_data_parsed = json.loads(entry.val)
                if 'GeneralObjectsDetected' in json_data_parsed['frameMetadata']:
                    for x in json_data_parsed['frameMetadata']['GeneralObjectsDetected']:
                        print(x)
                        obj = x.split(":", 0)
                        print(obj)
                        #self.generalObjectsFound.add(obj)

        except:
            self.logger.info("Failed to scan table in Accumulo! Shutting down conn")
            raise ValueError("Failed to scan table in Accumulo! Shutting down conn")
            self.conn.close()
        print(self.generalObjectsFound)
        self.conn.close()
        
        
    def performAnalysis(self, table):
        self.logger.info("Performing video analysis...")
        #self.calculateAverageTargetConfidence(table)  #calculates average target confidence and finds the highest/lowest target confidence with their specific frame number
        self.AverageGenObjectConfidence(table)
        
        
    def run(self, table):
        if self.readyForAnalysis(table):
            self.performAnalysis(table)



def main():
    vidanalysis = videoAnalysis()
    vidanalysis.run("vid7_mp4")

   
if __name__ == "__main__":
    main()
    
