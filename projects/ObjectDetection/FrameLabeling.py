# import the necessary packages
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


# renamed class and file to FrameLabeling
class FrameLabeling(object):
    
    def __init__(self): #prototxt, model, labels
        """ Constructor """
        self.validate_arg_parse()
    
    def validate_arg_parse():
        """ Validates arg parser """
        # Parser to parse arguments passed
        parser = argparse.ArgumentParser()     
    
        parser.add_argument('--model',
            help = 'Path to model', 
            type = str,
            required = True)
        
        parser.add_argument('--model_prototxt',
            help = 'Path to prototxt file',
            type = str,
            required = True)
 
        parser.add_argument('--labels', 
            help = "path to list of class labels",
            type = str,
            required = True)
        
        parser.add_argument('--size', 
            help = "size of image after resize for normalization",
            type = int,
            required = False, 
            default = 300)
        
        parser.add_argument('--scalar', 
            help = "scalar adjustment for image normalization",
            type = float, 
            required = False, 
            default = 0.007843)
        
        parser.add_argument('--mean_subtraction', 
            help = "mean color channel subtraction for image normalization",
            type = float, 
            required = False, 
            default = 127.5)
        
        parser.add_argument('--condfidence',
            help = "minimum confidence for detections",
            type = float,
            required = False,
            default = .3)
        
        parser.add_argument('--topic_name_in',
            help = "topic that it is pulling from",
            type = str,
            required = False,
            default = "general")
    
        args = parser.parse_args()
        
        self.image = None
        self.b64 = None
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.classes = open(labels).read().strip().split('\n')
        
        if args.model:
            self.model = args.model
        if args.model_prototxt:
            self.prototxt = args.model_prototxt
        if args.labels:
            self.classes = open(args.labels).read().strip().split('\n')
        if args.size:
            self.size = args.size
        if args.scalar:
            self.scalar = args.scalar
        if args.mean_subtraction:
            self.mean_subtraction = args.mean_subtraction
        if args.scalar:
            self.scalar = args.scalar
        if args.condidence:
            self.confidenceThreshold = args.condfidence
        if args.model && args.model_prototxt:
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        if args.topic_name_in:
            self.topic_name_in = args.topic_name_in

    def run_frame_labeling(self, json_data_parsed):
        """ Runs frames for labeling """
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        (h, w) = self.image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(self.image, (self.size, self.size)), self.mean_subtraction, (self.size, self.size), self.scalar)  # replaced hard  coded values for variables
        net.setInput(blob)
        detections = net.forward()
        labelingOccurred = False
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidenceThreshold:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                if idx >= 1 and idx <= 20:     # display the prediction and avoids index 0 which is 'background'
                    labelingOccurred = True
                    label = "{}: {:.2f}%".format(self.classes[idx], confidence*100)
                    print("[INFO] {}".format(label))
                    cv2.rectangle(self.image, (startX, startY), (endX, endY), self.colors[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(self.image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.colors[idx], 2)
        if labelingOccurred:
            labeledb64 = base64.b64encode(self.image)    # may need to write some logic here in order to avoid adding to the json if no labeling occurred.
            json_data_parsed['LabeledImage'] = labeledb64   # adds base64 string to json data
           
    def run_images(self):      
        """ Runs each image """
        print("\n Consuming messages from 'general'\n")
        consumer = Consumer.initialize(self.topic_name_in)
        for m in consumer:
            json_data = m.value     
            json_data_parsed = json.loads(json_data)
            print("\n Running frame labeling against frame: " + str(json_data_parsed['frameNum']) + "\n")
            frame = Utilities.decodeFrameForObjectDetection(json_data_parsed)
            self.image = frame
            self.run_frame_labeling(json_data_parsed)
            json_data = json.dumps(json_data_parsed)
            Utilities.storeJson(json_data, "../../res/FramesMetadataLabelingFrame/" + json_data_parsed['videoName'] + "_Metadata.txt") 
        consumer.close()
        print("\nFrame labeling consumer closed!")

    
def main():
    """ Auto run main method """
    obj = FrameLabeling()
    obj.run_images()
    # ** TODO: Add database (Accumulo and Scylla) here by pushing finalized json data to database **


if __name__=="__main__":
    main()

