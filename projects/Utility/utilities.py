import cv2
import json
import ntpath
import base64
import argparse
import sys
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
from kafka_manager import *

class Utilities(object):

    @staticmethod
    def storeJson(frameMetadataJsonList, filePath):
        print("Storing metadata Json files locally... \n")
        file1 = open(filePath, 'w')   # open file handler for specific filePath
        for i in range(len(frameMetadataJsonList)):     # loop through the list of the frames metadata Jsons and write them to the the file
            file1.write(str(frameMetadataJsonList[i]) + "\n\n")
        file1.close()

    
    @staticmethod
    def exportJson(frameMetadataJsonList, topic):
        print("Exporting metadata Json files to kafka topic: " + str(topic) + "... \n")
        for i in range(len(frameMetadataJsonList)):     # loop through the list of the frames metadata Jsons and push to specific kafka topic
            print("Exporting frame " + str(i))
            Producer.push_json(topic, frameMetadataJsonList[i]) 