from label_image import main as labelImage

import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


class TargettedObjectDetection(object):
    
    def __init__(self):
        """ Constructor """
        self.validate_arg_parse()
        
    def validate_arg_parse(self):
        """ Validates arg parser """
        parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    
        parser.add_argument('--graph', 
            help = 'Path to video for processing',
            type = str, 
            required = True)
    
        parser.add_argument('--labels', 
            help = 'Path to model labels',
            type = str, 
            required = True)
        
        parser.add_argument('--input_layer', 
            help = 'Input layer name',
            type = str,
            required = True)
    
        parser.add_argument('--output_layer', 
            help = 'Output layer name',
            type = str, 
            required = True)
        
        parser.add_argument('--input_height', 
            help = 'Input height neccessary for type of model', 
            type = int,
            required = True)
        
        parser.add_argument('--input_width', 
            help = 'Input width neccessary for type of model',
            type = int, 
            required = True)
        
        parser.add_argument('--topic_name_in', 
            help = "topic that it is pulling from",
            type = str,
            required = False,
            default = "framefeeder")
        
        parser.add_argument('--topic_name_out', 
            help = "topic that it is pushing to",
            type = str,
            required = False,
            default = "target2")
            
        args = parser.parse_args()
    
        if args.graph:
            Utilities.verifyPath(args.graph)
            self.graph = args.graph
        if args.labels:
            Utilities.verifyPath(args.labels)
            self.labels = args.labels
        if args.input_layer:
            self.input_layer = args.input_layer
        if args.output_layer:
            self.output_layer = args.output_layer
        if args.input_height:
            self.input_height = args.input_height
        if args.input_width:
            self.input_width = args.input_width
        if args.topic_name_in:
            self.topic_name_in = args.topic_name_in
        if args.topic_name_out:
            self.topic_name_out = args.topic_name_out
    
    def run(self):
        """ Runs targetted obj detection """
        print("\nConsuming messages from 'framefeeder'")
        consumer = Consumer.initialize(self.topic_name_in)
        for m in consumer:
            json_data = m.value   # pull jsons from kafka topic into list for processing
            json_data_parsed = json.loads(json_data)   # loads json data into a parsed string (back to dict)
            frame = Utilities.decodeFrame(json_data_parsed)    # take parsed string and send it to utilities to decode it from base64 
            frameAsTensor = tf.image.decode_jpeg(frame, channels=3)   # convert frame to Tensor as string
            print("\n Running labelImage against frame: " + str(json_data_parsed['frameMetadata']['frameNum']) + "\n")        
            confidenceStat = labelImage(self.graph, self.labels, self.input_layer, self.output_layer, self.input_height, self.input_width, frameAsTensor)    # tests frame for targeted object
            if confidenceStat != None:     # if the target object was found within the threshold confidence, append that information to the JSON file. 
                json_data_parsed['frameMetadata']['foundTargetWithConfidence'] = str(confidenceStat)
                json_data = json.dumps(json_data_parsed)
            Utilities.storeJson(json_data, "../../res/FramesMetadataTargetImgClassification/" + json_data_parsed['videoMetadata']['videoName'] + "_Metadata.txt")    # Store updated metadata Jsons locally
            Utilities.exportJson(json_data, self.topic_name_out)    # export updated Json files to kafka topic 'target'
        consumer.close()
        print("\nTargetted Object Detection consumer closed!")


def main():
    """ Auto run main method """
    obj = TargettedObjectDetection()
    obj.run()


if __name__ == "__main__":
    main()
