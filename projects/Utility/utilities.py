from __future__ import division
import cv2
import json
import ntpath
import base64
import argparse
import sys
import time
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
from kafka_manager import *

class Utilities(object):
    
    @staticmethod
    def runProgressbar(percent):
        sys.stdout.write("\r%d%%" % percent)
        sys.stdout.flush()
        
        

    @staticmethod
    def storeJson(frameMetadataJsonList, filePath):
        print("\nStoring metadata Json files locally... ")
        file1 = open(filePath, 'w')   # open file handler for specific filePath
        for i in range(len(frameMetadataJsonList)):     # loop through the list of the frames metadata Jsons and write them to the the file
            file1.write(str(frameMetadataJsonList[i]) + "\n\n")
        file1.close()

    
    @staticmethod
    def exportJson(frameMetadataJsonList, topic):
        print("\nExporting metadata Json files to kafka topic: " + str(topic) + "... ")
        for i in range(int(len(frameMetadataJsonList))):     # loop through the list of the frames metadata Jsons and push to specific kafka topic
            Producer.push_json(topic, frameMetadataJsonList[i]) 
            Utilities.runProgressbar((i / len(frameMetadataJsonList)) * 100)
            
            
    @staticmethod
    def encodeImage (frameimage):
        to_encode = cv2.imencode(".jpg",frameimage)
        string64 = base64.b64encode(to_encode)
        return string64
    
    