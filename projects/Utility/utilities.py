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
    def storeJson(frameJson, filePath):
        file1 = open(filePath, 'a+')   # open file handler for specific filePath
        file1.write(str(frameJson) + "\n\n")
        file1.close()

    
    @staticmethod
    def exportJson(frameJson, topic):
            Producer.push_json(topic, frameJson) # Push frame json to specified Kafka topic
            
    @staticmethod
    def encodeImage (frameimage):
        to_encode = cv2.imencode(".jpg",frameimage)
        string64 = base64.b64encode(to_encode)
        return string64
    
    
    