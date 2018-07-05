# USAGE
# python deep_learning_with_opencv.py --image images/jemma.png --prototxt bvlc_googlenet.prototxt --model bvlc_googlenet.caffemodel --labels synset_words.txt

# import the necessary packages
import numpy as np
import argparse
import cv2
import base64
import json
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

class GeneralImageClassification(object):
        
    def __init__(self, prototxt, model):
        self.image = "../../res/genimg.jpg"
        self.prototxt = prototxt
        self.model = model
        self.labels = "../../res/synset_words.txt"
		self.size = 300
		self.mean_subtraction = 0.007843
		self.scalar = 127.5


    def run_object_detection(self, json_data_parsed):
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        img = cv2.imread(self.imagePath)
 #       (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (self.size, self.size)), self.mean_subtraction, (self.size, self.size), self.scalar)
        net.setInput(blob)
        detections = net.forward()
		label_list = list()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidenceThreshold:
                idx = int(detections[0, 0, i, 1])
#                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                (startX, startY, endX, endY) = box.astype("int")
                # display the prediction
                print("idx = " + str(idx))
#               if idx >= 0 and idx <= 20:
                label = "{}: {:.2f}%".format(self.classes[idx], confidence*100)
#               print("[INFO] {}".format(label))
				label_list.append(label)
#                    cv2.rectangle(img, (startX, startY), (endX, endY), self.colors[idx], 2)
#                    y = startY - 15 if startY - 15 > 15 else startY + 15
#                    cv2.putText(img, label, (startX, y),
#                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors[idx], 2)
        json_data_parsed ['ObjectsDetected'] = label_list

    def run_images(self):
        print("Consuming messages from 'target2'\n")
        consumer = Consumer.initialize("target2")
        for m in consumer:
            json_data = m.value     
            print("\n Running object detection model against the frames")
            json_data_parsed = json.loads(json_data)
            frame = Utilities.decodeFrame(json_data_parsed)     # TODO: change this so that we dont have to write a file. 
            fh = open(self.image, "wb")
            fh.write(frame)
            fh.close()                        
            self.run_object_detection(json_data_parsed)
			json_data = json.dumps(json_data_parsed)
            Utilities.exportJson(json_data, "general")    # currently exports same data read from kafka topic until we know what to add from this component
         
            
            
    
def main():
    prototxt = "../../res/MobileNetSSD_deploy.prototxt.txt"
    model = "../../res/MobileNetSSD_deploy.caffemodel"    
    obj = GeneralImageClassification(prototxt,model)
    obj.run_images()



if __name__=="__main__":
        main()
