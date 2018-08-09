# USAGE
# python deep_learning_with_opencv.py --image images/jemma.png --prototxt bvlc_googlenet.prototxt --model bvlc_googlenet.caffemodel --labels synset_words.txt

from ..Utility.utilities import *


# changed class from ImageClassification to ObjectDetection
# uses the code for  FrameLabeling as a base
class GeneralObjectDetection(object):

    # added missing variables (classes, confidenceThreshold)
    # extracted and added variables for size, mean_subtraction, and scalar
    def __init__(self):
        """ Constructor """
        self.logger = Utilities.setup_logger("general-obj", "../../logs/GeneralObjectDetection.log")
        self.validate_arg_parse()

    def validate_arg_parse(self):
        """ Validates arg parser """
        # Parser to parse arguments passed
        parser = argparse.ArgumentParser()

        parser.add_argument('--model',
                            help='Path to model',
                            type=str,
                            required=True)

        parser.add_argument('--model_prototxt',
                            help='Path to prototxt file',
                            type=str,
                            required=True)

        parser.add_argument('--labels',
                            help="path to list of class labels",
                            type=str,
                            required=True)

        parser.add_argument('--size',
                            help="size of image after resize for normalization",
                            type=int,
                            required=False,
                            default=300)

        parser.add_argument('--scalar',
                            help="scalar adjustment for image normalization",
                            type=float,
                            required=False,
                            default=0.007843)

        parser.add_argument('--mean_subtraction',
                            help="mean color channel subtraction for image normalization",
                            type=float,
                            required=False,
                            default=127.5)

        parser.add_argument('--confidence',
                            help="minimum confidence for detections",
                            type=float,
                            required=False,
                            default=0.01)

        parser.add_argument('--topic_name_in',
                            help="topic that it is pulling from",
                            type=str,
                            required=False,
                            default="target2")

        parser.add_argument('--topic_name_out',
                            help="topic that it is pushing to",
                            type=str,
                            required=False,
                            default="general")

        args = parser.parse_args()
        self.image = None

        if args.model:
            Utilities.verifyPath(args.model, self.logger)
            self.model = args.model
        if args.model_prototxt:
            Utilities.verifyPath(args.model_prototxt, self.logger)
            self.prototxt = args.model_prototxt
        if args.labels:
            Utilities.verifyPath(args.labels, self.logger)
            self.classes = open(args.labels).read().strip().split('\n')
        if args.size:
            self.size = args.size
        if args.scalar:
            self.scalar = args.scalar
        if args.mean_subtraction:
            self.mean_subtraction = args.mean_subtraction
        if args.scalar:
            self.scalar = args.scalar
        if args.confidence:
            self.confidenceThreshold = args.confidence
        if args.model and args.model_prototxt:
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
        if args.topic_name_in:
            self.topic_name_in = args.topic_name_in
        if args.topic_name_out:
            self.topic_name_out = args.topic_name_out

    # removed all code related to label, or creating bounding boxes
    # added json_data_parsed to method parameters
    def run_object_detection(self, json_data_parsed):
        """ Runs the general object detection on a frame """
        # replaced values with variables
        blob = cv2.dnn.blobFromImage(cv2.resize(self.image,
                                                (self.size, self.size)), self.scalar, (self.size, self.size),
                                     self.mean_subtraction)
        self.net.setInput(blob)
        detections = self.net.forward()
        # create a list to store found labels
        label_list = []
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > self.confidenceThreshold:
                idx = int(detections[0, 0, i, 1])
                if idx >= 1 and idx <= 20:  # display the prediction
                    label = "{}: {:.2f}%".format(self.classes[idx], confidence * 100)
                    self.logger.info("    [INFO] {}".format(label))
                    label_list.append(label)  # adds new label to label_list
        if label_list:  # if label_list is not empty (meaning gen objects were found), then add to json
            json_data_parsed['frameMetadata']['GeneralObjectsDetected'] = label_list  # appends label_list to JSON data

    def run_images(self):
        """ Runs each image through the general object detection """
        self.logger.info("Consuming messages from '%s'" % self.topic_name_in)
        consumer = Consumer.initialize(self.topic_name_in)
        for m in consumer:
            json_data = m.value
            json_data_parsed = json.loads(json_data)
            self.logger.info(
                "Running General Object Det against frame: " + str(json_data_parsed['frameMetadata']['frameNum']))
            frame = Utilities.decodeFrameForObjectDetection(
                json_data_parsed)  # this utility method will not only decode the b64 string, but also prepare the image to be compatible with opencv
            self.image = frame
            self.run_object_detection(json_data_parsed)
            json_data = json.dumps(json_data_parsed)  # writes json_data_parsed to the JSON file
            Utilities.storeJson(json_data,
                                "../../res/FramesMetadataGenObjDetections/" + json_data_parsed['videoMetadata'][
                                    'videoName'] + "_Metadata" + str(
                                    json_data_parsed['frameMetadata']['frameNum']) + ".txt")
            Utilities.exportJson(json_data,
                                 self.topic_name_out)  # exports JSON file with the list of labels for the identified objects
        consumer.close()
        self.logger.info("General Object Detection consumer closed")


def main():
    """ Auto run main method """
    obj = GeneralObjectDetection()
    obj.run_images()


if __name__ == "__main__":
    main()
