# import the necessary packages
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


# renamed class and file to FrameLabeling
class FrameLabeling(object):

    def __init__(self, prototxt, model, labels):
        self.image = None
        self.prototxt = prototxt
        self.model = model
        self.classes = open(labels).read().strip().split('\n')
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.confidenceThreshold = 0.3
        self.b64 = ''
        # added variables for size, mean_subtraction, and scalar values for easy of change
        self.size = 300
        self.mean_subtraction = 0.007843
        self.scalar = 127.5
        

    def run_frame_labeling(self):
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        (h, w) = self.image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self.image, (self.size, self.size)), self.mean_subtraction, (self.size, self.size), self.scalar)  # replaced hard  coded values for variables
        net.setInput(blob)
        detections = net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidenceThreshold:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                if idx >= 1 and idx <= 20:     # display the prediction and avoids index 0 which is 'background'
                    label = "{}: {:.2f}%".format(self.classes[idx], confidence*100)
                    print("[INFO] {}".format(label))
                    print((startX, startY))
                    print((endX, endY))
                    print(self.colors[idx])
                    cv2.rectangle(self.image, (startX, startY), (endX, endY), self.colors[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(self.image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors[idx], 2)
        self.b64 = base64.b64encode(self.image)    # may need to write some logic here in order to avoid adding to the json if no labeling occurred.

                       
    def run_images(self):      
        print("\n Consuming messages from 'general'\n")
        consumer = Consumer.initialize("general")
        for m in consumer:
            json_data = m.value     
            json_data_parsed = json.loads(json_data)
            print("\n Running frame labeling against frame: " + str(json_data_parsed['frameNum']) + "\n")
            frame = Utilities.decodeFrameForObjectDetection(json_data_parsed)
            self.image = frame
            self.run_frame_labeling()
            json_data_parsed['LabeledImage'] = self.b64   # adds base64 string to json data
            json_data = json.dumps(json_data_parsed)
            Utilities.storeJson(json_data, "../../res/FramesMetadataLabelingFrame/" + json_data_parsed['videoName'] + "_Metadata.txt")     
        consumer.close()
        print("\nFrame labeling consumer closed!")
            
           

    
def main():
    parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    parser.add_argument('--model', type=str, help='Path to frame labeling object detection model')
    parser.add_argument('--model_prototxt', type=str, help='Path to model prototxt')
    parser.add_argument("--labels", type=str, help="path to list of class labels")
    args = parser.parse_args()
    obj = FrameLabeling(args.model_prototxt, args.model, args.labels)
    obj.run_images()
    # ** TODO: Add database (Accumulo and Scylla) here by pushing finalized json data to database **
    
if __name__=="__main__":
    main()

