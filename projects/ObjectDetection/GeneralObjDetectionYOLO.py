# USAGE
# python deep_learning_with_opencv.py --image images/jemma.png --prototxt bvlc_googlenet.prototxt --model bvlc_googlenet.caffemodel --labels synset_words.txt

# import the necessary packages
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *
from darknet import main as yoloObjDetection


# changed class from ImageClassification to ObjectDetection
# uses the code for  FrameLabeling as a base

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

lib = CDLL("../ObjectDetection/libdarknet.so", RTLD_GLOBAL)

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA


class GeneralObjectDetection(object):
    # added missing variables (classes, confidenceThreshold)
    # extracted and added variables for size, mean_subtraction, and scalar
    def __init__(self):
        """ Constructor - Initalizes prototxt and model """
        self.validate_arg_parse()
        
    def validate_arg_parse(self):
        """ Validates arg parser """
        # Parser to parse arguments passed
        parser = argparse.ArgumentParser()  
        
        parser.add_argument('--net', 
            help = 'Name of the net (cfg)',
            type = str, 
            required = True)
            
        parser.add_argument('--weights', 
            help = 'Name of the weights to use',
            type = str, 
            required = True)
            
        parser.add_argument('--meta', 
            help = 'Name of the dataset to use',
            type = str, 
            required = True)
            
        parser.add_argument('--topic_name_in', 
            help = 'topic that it is pushing to',
            type = str, 
            required = False,
            default = "target2")
            
        parser.add_argument('--topic_name_out', 
            help = 'topic that it is pushing to',
            type = str, 
            required = False,
            default = "general")
        
        args = parser.parse_args()
                
        if args.net:
            #Utilities.verifyPath(args.video)
            self.net = args.net
        if args.weights:
            self.weights = args.weights
        if args.meta:
            self.meta = args.meta
        if args.topic_name_in:
            self.topic_name_in = args.topic_name_in
        if args.topic_name_out:
            self.topic_name_out = args.topic_name_out
            
        self.image = None


    def run_objectDetection(self, json_data_parsed):
       label_list = []
       results = yoloObjDetection(self.net, self.meta, self.image)
       if results:
           json_data_parsed['frameMetadata']['GeneralObjectsDetected'] = results
              
       
        

    def run_images(self):
        """ Runs each image through the general object detection """
        consumer = Consumer.initialize(self.topic_name_in)
        print("Consuming messages from 'target2'\n")
        self.net = load_net(self.net, self.weights, 0)  #load net initially to avoid loading net over and over again
        self.meta = load_meta(self.meta)      #load meta initially to avoid loading meta over and over again
        print("Finished loading net and meta for YOLO\n")
        for m in consumer:
            json_data = m.value     
            json_data_parsed = json.loads(json_data)
            print("\n Running General Object Det against frame: " + str(json_data_parsed['frameMetadata']['frameNum']) + "\n")
            frame = Utilities.decodeFrameForObjectDetection(json_data_parsed)
            self.image = frame
            self.run_objectDetection(json_data_parsed)
            json_data = json.dumps(json_data_parsed)
            Utilities.storeJson(json_data, "../../res/FramesMetadataGenObjDetections/" + json_data_parsed['videoMetadata']['videoName'] + "_Metadata.txt") 
            Utilities.exportJson(json_data, self.topic_name_out)
        consumer.close()
        print("\nGeneral Object Detection consumer closed!")
        
                      
    
def main():
    obj = GeneralObjectDetection()
    obj.run_images()     


if __name__=="__main__":
        main()
