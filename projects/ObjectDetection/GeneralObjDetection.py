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
        self.image = None
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
		# replaced values with variables
        blob = cv2.dnn.blobFromImage(cv2.resize(self.image, (self.size, self.size)), self.mean_subtraction, (self.size, self.size), self.scalar)
        net.setInput(blob)
        detections = net.forward()
		# create a list to store found labels
        label_list = []
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
            json_data_parsed = json.loads(json_data)
            frame = Utilities.decodeFrameForObjectDetection(json_data_parsed)   # this utility method will not only decode the b64 string, but also prepare the image to be compatible with opencv
            self.image = frame
            self.run_object_detection(json_data_parsed)
            json_data = json.dumps(json_data_parsed)  # writes json_data_parsed to the JSON file
            Utilities.storeJson(json_data, "../../res/FramesMetadataGenObjDetection/frameMetadata.txt")
            Utilities.exportJson(json_data, "general")   # exports JSON file with the list of labels for the identified objects
        consumer.close()
        print("\nGeneral Object Detection consumer closed!")
         
            
          
def main():
    parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    parser.add_argument('--model', type=str, help='Path to prototxt file')
    parser.add_argument('--model_prototxt', type=str, help='Path to model')
    args = parser.parse_args()
    obj = GeneralObjectDetection(args.model_prototxt, args.model)
    obj.run_images()


if __name__=="__main__":
        main()
