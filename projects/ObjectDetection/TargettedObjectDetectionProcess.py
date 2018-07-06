from label_image import main as labelImage

import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

    
def main():
    parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    parser.add_argument('--graph', type=str, help='Path to video for processing')
    parser.add_argument('--labels', type=str, help='Path to model labels')
    parser.add_argument('--input_layer', type=str, help='Input layer name')
    parser.add_argument('--output_layer', type=str, help='Output layer name')
    parser.add_argument('--input_height', type=int, help='Input height neccessary for type of model')
    parser.add_argument('--input_width', type=int, help='Input width neccessary for type of model')
    
    args = parser.parse_args()
    if args.graph:
        graph = args.graph
    if args.labels:
        labels = args.labels
    if args.input_layer:
        input_layer = args.input_layer
    if args.output_layer:
        output_layer = args.output_layer
    if args.input_height:
        input_height = args.input_height
    if args.input_width:
        input_width = args.input_width	
    
    print("\nConsuming messages from 'framefeeder'")
    consumer = Consumer.initialize("framefeeder")
    for m in consumer:
        json_data = m.value   # pull jsons from kafka topic into list for processing
        json_data_parsed = json.loads(json_data)   # loads json data into a parsed string (back to dict)
        frame = Utilities.decodeFrame(json_data_parsed)    # take parsed string and send it to utilities to decode it from base64 
        frameAsTensor = tf.image.decode_jpeg(frame, channels=3)   # convert frame to Tensor as string
        print("running labelImage against a frame\n")
        confidenceStat = labelImage(graph, labels, input_layer, output_layer, input_height, input_width, frameAsTensor)    # tests frame for targeted object
        if confidenceStat != None:     # if the target object was found within the threshold confidence, append that information to the JSON file. 
            json_data_parsed['foundTargetWithConfidence'] = str(confidenceStat)
            json_data = json.dumps(json_data_parsed)
        Utilities.storeJson(json_data, "../../res/frameMetadataListTargetOBJD.txt")    # Store updated metadata Jsons locally
        Utilities.exportJson(json_data, "target2")    # export updated Json files to kafka topic 'target'
        print(json_data_parsed['frameNum'])   # print frame number that was just processed
    consumer.close()
    print("\nTargetted Object Detection consumer closed!")
        

if __name__ == "__main__":
    main()
    
