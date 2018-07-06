from __future__ import division
import numpy as np
import tensorflow as tf
import cv2
import json
import ntpath
import base64
import argparse
import os
import sys
import time
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
from kafka_manager import *

class Utilities(object):


    @staticmethod
    def storeJson(frameJson, filePath):
        """ Stores the json to a filepath """
        file1 = open(filePath, 'a+')   # open file handler for specific filePath
        file1.write(str(frameJson) + "\n\n")
        file1.close()


    @staticmethod
    def exportJson(frameJson, topic):
        """ Exports the json to a topic """
        Producer.push_json(topic, frameJson) # Push frame json to specified Kafka topic


    @staticmethod
    def encodeFrame(frame):
        """ Encodes the image using base 64 """
        return base64.b64encode(frame)


    @staticmethod
    def decodeFrame(frameJson):
        """ Decodes the image using base 64 """
        frameBase64 = frameJson["imageBase64"]
        return base64.b64decode(frameBase64)

    @staticmethod
    def decodeFrameForObjectDetection(frameJson):
        """ Decodes the image using base 64 """
        img = frameJson["imageBase64"]
        nparr = np.fromstring(img.decode('base64'), np.uint8)
        newImage = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return newImage
