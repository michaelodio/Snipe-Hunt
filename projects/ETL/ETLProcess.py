from ..Utility.utilities import *

extensions = [".mp4", ".mpg", ".mov", ".wmv"]  # global variables for movie extensions


class VideoETL(object):

    def __init__(self):
        """ Constructor """
        self.logger = Utilities.setup_logger("etl", '../../logs/ETL.log')
        self.validate_arg_parse()

    def validate_arg_parse(self):
        """ Validates arg parser """
        # Parser to parse arguments passed
        parser = argparse.ArgumentParser()

        parser.add_argument('--topic_name_in',
                            help='Path to video or folder of videos for processing',
                            type=str,
                            required=False,
                            default="pathfinder")

        parser.add_argument('--topic_name_out',
                            help='topic that it is pushing to',
                            type=str,
                            required=False,
                            default="framefeeder")

        args = parser.parse_args()
        self.videoPath = ""

        if args.topic_name_in:
            self.topic_name_in = args.topic_name_in
        if args.topic_name_out:
            self.topic_name_out = args.topic_name_out

    def splitFrames(self):
        """ Splits up the frames """
        self.logger.info("Splitting Frames and extracting metadata...")
        cap = cv2.VideoCapture(self.videoPath)  # open video in openCV
        totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # grab total frames in the video
        if cap.isOpened is False:
            self.logger.error("Cannot open video stream or file in ETL")
        for x in range(totalFrame):  # loop through all of the frames and extract meta data on each frame
            retval, videoframe = cap.read()  # grab the next frame
            self.extractFrameMetadata(videoframe, totalFrame, cap)  # collect metadata on the frame
        cap.release()
        self.logger.info("Finished splitting frames")

    def extractFrameMetadata(self, videoframe, totalFrame, cap):
        """ Extracts the metadata from the frame """
        frameNum = int(cap.get(cv2.CAP_PROP_POS_FRAMES))  # collect the current frame number
        self.logger.info("    Splitting and extracting metadata on frame number: " + str(frameNum))
        FPS = int(cap.get(cv2.CAP_PROP_FPS))  # grab the frames per second of the video
        videoDuration = round(totalFrame / FPS)  # calculate the video's duration
        relativePosition = "%.2f" % (frameNum / totalFrame)  # calculate this frames relative position in the video
        videoName = os.path.basename(self.videoPath)  # collect the videos name
        timeStamp = round(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000  # collect time stamp and convert it to seconds
        retval, frameConvertedToJPG = cv2.imencode('.jpg',
                                                   videoframe)  # encode frame to .jpg for base64string conversion
        frameAsBase64String = Utilities.encodeFrame(frameConvertedToJPG)  # encode frame to base64String
        videoMetadata = {}
        frameMetadata = {}
        metadata = {}
        videoMetadata['videoPath'] = self.videoPath
        videoMetadata['videoName'] = videoName
        videoMetadata['videoDuration'] = str(videoDuration) + " seconds"
        videoMetadata['totalFrames'] = totalFrame
        videoMetadata['FPS'] = FPS
        frameMetadata['frameNum'] = frameNum
        frameMetadata['timestamp'] = str(timeStamp) + " seconds"
        frameMetadata['relativePosition'] = relativePosition
        metadata['videoMetadata'] = videoMetadata
        metadata['frameMetadata'] = frameMetadata
        metadata['imageBase64'] = frameAsBase64String
        frameJson = json.dumps(metadata)  # create frame json with collected metadata
        Utilities.exportJson(frameJson, self.topic_name_out)  # export frame json to kafka topic
        Utilities.storeJson(frameJson, "../../res/FramesMetadataETL/" + videoName + "_Metadata" + str(
            frameNum) + ".txt")  # store frame json locally

    def run(self):
        """ Launches the ETL Process """
        self.logger.info("Consuming messages from '%s'" % self.topic_name_in)
        consumer = Consumer.initialize(self.topic_name_in)
        for m in consumer:
            self.videoPath = m.value
            self.videoPath = self.videoPath[1:-1]
            self.logger.info("Pulled Message: '%s'" % self.videoPath)
            if self.videoPath.endswith(tuple(extensions)):
                self.splitFrames()


def main():
    """ Auto run main method """
    etl = VideoETL()
    etl.run()


if __name__ == "__main__":
    main()
