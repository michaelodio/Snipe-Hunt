from label_image import main as labelImage
import os
import cv2
import base64
import json
import numpy as np
import sys
import numpy as np
import tensorflow as tf
import time
sys.path.insert(0, "../DataTransfer")   # used to import files from other folder (DataTransfer) dir in project
from kafka_manager import *



graph = "../../res/TfModel/output_graph.pb"
labels = "../../res/TfModel/output_labels.txt"
input_layer = "Placeholder"
output_layer = "final_result"
input_height = 224   # Neccessary input_height for mobilnet model
input_width = 224    # Neccessary input_wifth for mobilenet model



def main():
    print("Consuming messages from 'framefeeder'\n")
    json_data_list = Consumer.pull_jsons("framefeeder")   # pull jsons from kafka topic into list for processing
    print("Running labelImage against all frames \n")
    for i in range(len(json_data_list)):
        json_data_parsed = json.loads(json_data_list[i])   # loads json data into a parsed string (back to dict)
        frameBase64 = json_data_parsed["imageBase64"]   # extracts base64 string of image (frame)
        frame = base64.b64decode(frameBase64)         # decodes base64 image
        fh = open("../../res/testingB64decode.jpeg", "wb")   # used for writing decoded base64 image locally to then be tested against with label_image()
        fh.write(frame)        # writes decoded image to file in order to pass filepath to label_Image script
        fh.close()
        print("FrameNum: " + str(i))    # display which frame is being targeted object detected against
        confidenceStat = labelImage(graph, labels, input_layer, output_layer, input_height, input_width, "../../res/testingB64decode.jpeg")    # tests frame for targeted object
        if confidenceStat != None:     # if the target object was found within the threshold confidence, append that information to the JSON file. 
            json_data_parsed['foundTargetWithConfidence'] = str(confidenceStat)
            print(json_data_parsed)
        

if __name__ == "__main__":
    main()