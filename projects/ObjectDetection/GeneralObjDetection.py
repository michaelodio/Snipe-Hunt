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
    def __init__(self, prototxt, model, labels):
        """ Constructor - Initalizes prototxt and model """
        self.image = None
        self.prototxt = prototxt
        self.model = model
        self.labels = labels


    def run_classification(self):
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        rows = open(self.labels).read().strip().split("\n")
        classes = [r[r.find(" ") + 1:].split(",")[0] for r in rows]
        newimg = cv2.resize(self.image,(224,224))
        blob = cv2.dnn.blobFromImage(newimg, 1, (224, 224), (104, 117, 123))      
        net.setInput(blob)
        preds = net.forward()
        idxs = np.argsort(preds[0])[::-1][:1]
        for (i, idx) in enumerate(idxs):
            if i == 0:
                output = "Label: {}, {:.2f}%".format(classes[idx], preds[0][idx] * 100)
                cv2.putText(self.image, output, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
       # print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1,classes[idx], preds[0][idx]))        
           # cv2.imshow("Image", image)
               #cv2.waitKey(0)
    #print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1,
        #classes[idx], preds[0][idx]))
            print("[INFO] {}. label: {}, probability: {:.5}".format(i + 1,classes[idx], preds[0][idx] * 100))
        #cv2.imshow("Image", self.image)  
        #cv2.waitKey(0)
        

    def run_images(self):
        """ Runs each image through the general object detection """
        consumer = Consumer.initialize("target2")
        print("Consuming messages from 'target2'\n")
        for m in consumer:
            json_data = m.value     
            json_data_parsed = json.loads(json_data)
            frame = Utilities.decodeFrameForObjectDetection(json_data_parsed)
            self.image = frame
            self.run_classification()
            Utilities.storeJson(json_data, "../../res/FramesMetadataGenObjDetections/framesMetadata.txt") 
            Utilities.exportJson(json_data, "general")
        consumer.close()
        print("\nGeneral Object Detection consumer closed!")
        
                      
    
def main():
    prototxt = "../../res/bvlc_googlenet.prototxt"
    model = "../../res/bvlc_googlenet.caffemodel"
    labels = "../../res/synset_words.txt"
    obj = GeneralObjectDetection(prototxt, model, labels)
    obj.run_images()     


if __name__=="__main__":
        main()
