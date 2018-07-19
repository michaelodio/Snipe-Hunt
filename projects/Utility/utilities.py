from __future__ import division  # used to avoid integer divsion truncation and adds '//' to force it
import numpy as np
import tensorflow as tf
import cv2
import json
import ntpath
import base64
from PIL import Image
import argparse
from ctypes import *
import math
import random
import os
import sys
import time
import logging
from pyaccumulo import Accumulo, Mutation, Range
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
from kafka_consumer import *
from kafka_producer import *

class Utilities(object):


    @staticmethod
    def storeJson(frameJson, filePath):
        """ Stores the json to a filepath """
        file1 = open(filePath, 'a+')   # open file handler for specific filePath
        file1.write(str(frameJson) + "\n")
        file1.close()


    @staticmethod
    def exportJson(frameJson, topic):
        """ Exports the json to a topic """
        push_json(Producer.initialize(), topic, frameJson) # Push frame json to specified Kafka topic


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

    @staticmethod
    def get_file_paths(directory):
        storePaths = []
        extensions = [".mp4", ".mpg", ".mov", ".wmv"]
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(tuple(extensions)):
                    storePaths.append(os.path.join(root, f))
        return storePaths
        
    @staticmethod
    def verifyPath(path, logger):
        if not os.path.exists(path):
            logger.error("File path: " + path + " does not exist")  #log this
            raise ValueError("File path: " + path + " does not exist") 
    
                
    @staticmethod
    def setup_logger(name, log_file, level=logging.INFO):
        """ Function setup as many loggers as want """
    
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('%(asctime)s    %(levelname)s: %(message)s'))
    
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        
        return logger
        
        
    @staticmethod
    def exportJsonDB(json_data, frameNum):
        conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")
        table = json.loads(json_data)['videoMetadata']['videoName']
        table = table.replace('.', '_')
        table = table.encode('ascii', 'ignore')
        if not conn.table_exists(table):
            conn.create_table(table)
        m = Mutation("row_%d"%frameNum)
        m.put(cf="cf1", cq="cq1", val=json_data)
        conn.write(table, m)
        conn.close()
        
        
    @staticmethod
    def printTableDB(table):
        conn = Accumulo(host="localhost", port=50096, user="root", password="RoadRally4321")
        for entry in conn.scan(table):
            print(entry.row, entry.cf, entry.cq, entry.cv, entry.ts, entry.val)
        conn.close()
    
