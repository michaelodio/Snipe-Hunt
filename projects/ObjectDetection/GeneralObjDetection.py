# USAGE
# python deep_learning_with_opencv.py --image images/jemma.png --prototxt bvlc_googlenet.prototxt --model bvlc_googlenet.caffemodel --labels synset_words.txt
# import the necessary packages
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


# changed class from ImageClassification to ObjectDetection
# uses the code for  FrameLabeling as a base
class GeneralObjectDetection(object):
        # added missing variables (classes, confidenceThreshold)
		# extracted and added variables for size, mean_subtraction, and scalar
    def __init__(self, prototxt, model):
        self.image = "../../res/genimg.jpg"
        self.prototxt = prototxt
        self.model = model
        self.classes = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]
        self.size = 300
        self.mean_subtraction = 0.007843
        self.scalar = 127.5
        self.confidenceThreshold = 0.3


		# removed all code related to label, or creating bounding boxes
		# added json_data_parsed to method parameters
    def run_object_detection(self, json_data_parsed):
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        img = cv2.imread(self.image)
		# replaced values with variables
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (self.size, self.size)), self.mean_subtraction, (self.size, self.size), self.scalar)
        net.setInput(blob)
        detections = net.forward()
		# create a list to store found labels
        label_list = list()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidenceThreshold:
                idx = int(detections[0, 0, i, 1])
                if idx >= 0 and idx <= 20:      # display the prediction
                    label = "{}: {:.2f}%".format(self.classes[idx], confidence*100)
                    print("[INFO] {}".format(label))
                    label_list.append(label)    # adds new label to label_list
        json_data_parsed['ObjectsDetected'] = label_list  # appends label_list to JSON data
            
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
            json_data = json.dumps(json_data_parsed)  # writes json_data_parsed to the JSON file
            Utilities.exportJson(json_data, "general")   # exports JSON file with the list of labels for the identified objects
         
            
          
def main():
    parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    parser.add_argument('--prototxt', type=str, help='Path to prototxt file')
    parser.add_argument('--model', type=str, help='Path to model')
    
    args = parser.parse_args()
    
    obj = GeneralImageClassification(args.prototxt, args.model)
    obj.run_images()


if __name__=="__main__":
        main()
