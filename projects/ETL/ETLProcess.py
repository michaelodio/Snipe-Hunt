import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

extensions = [".mp4", ".mpg", ".mov", ".wmv"]  # global variables for movie extensions

class VideoETL(object):

    def __init__(self): 
        """ Constructor """
        self.validate_arg_parse()
        Logger.initilaize('../../logs/ETL.log')
    
    def validate_arg_parse(self):
        """ Validates arg parser """
        # Parser to parse arguments passed
        parser = argparse.ArgumentParser()  
        
        parser.add_argument('--video', 
            help = 'Path to video or folder of videos for processing',
            type = str, 
            required = True)
            
        parser.add_argument('--topic_name_out', 
            help = 'topic that it is pushing to',
            type = str, 
            required = False,
            default = "framefeeder")
        
        args = parser.parse_args()
                
        if args.video:
            self.videoPath = args.video
        if args.topic_name_out:
            self.topic_name_out = args.topic_name_out

    def run(self):
        """ Runs the ETL process """
        '''
        FLAGS, unparsed = parser.parse_known_args()
        if ('videoFromUI' in keyword_parameters):    # if a videoPath was provided from the UI use that video path instead.
            FLAGS.video = keyword_parameters['videoFromUI']
        if FLAGS.video.endswith("/"):
            videosPath = Utilities.get_file_paths(FLAGS.video)
            for video in videosPath:
                videoEditor = VideoETL(video)   # create instance of VideoEditor object for processing the video with OpenCV
                videoEditor.splitFrames()   # splits the frames of the video as well as runs the extractFrameMetadata method on that frame.
        if FLAGS.video.endswith(tuple(extensions)):
            videoEditor = VideoETL(FLAGS.video)   # create instance of VideoEditor object for processing the video with OpenCV
            videoEditor.splitFrames()   # splits the frames of the video as well as runs the extractFrameMetadata method on that frame.
        '''

    def splitFrames(self):
        """ Splits up the frames """
        print("Splitting Frames and extracting metadata...\n")
        logging.info("Splitting Frames and extracting metadata...")
        cap = cv2.VideoCapture(self.videoPath)    # open video in openCV
        totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # grab total frames in the video
        if cap.isOpened is False:
            print("Error opening video stream or file")
            logging.error("Cannot open video stream or file")
        for x in range(totalFrame):     # loop through all of the frames and extract meta data on each frame
            retval, videoframe = cap.read()     # grab the next frame
            self.extractFrameMetadata(videoframe, totalFrame, cap)    # collect metadata on the frame
        cap.release()

    def extractFrameMetadata(self, videoframe, totalFrame, cap):
        """ Extracts the metadata from the frame """
        frameNum = cap.get(cv2.CAP_PROP_POS_FRAMES)   # collect the current frame number
        FPS = int(cap.get(cv2.CAP_PROP_FPS))     # grab the frames per second of the video
        videoDuration = round(totalFrame / FPS)   # calculate the video's duration
        relativePosition = "%.2f" % (frameNum / totalFrame)   # calculate this frames relative position in the video
        videoName = os.path.basename(self.videoPath) # collect the videos name
        timeStamp = round(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000    # collect time stamp and convert it to seconds
        retval, frameConvertedToJPG = cv2.imencode('.jpg', videoframe)   # encode frame to .jpg for base64string conversion
        frameAsBase64String = Utilities.encodeFrame(frameConvertedToJPG)    # encode frame to base64String
        frameJson = json.dumps({'videoPath': self.videoPath, 'videoName': videoName, 'videoDuration': str(videoDuration) + " seconds", 'totalFrames': totalFrame, 'FPS': FPS, 'frameNum': frameNum, 'timeStamp': str(timeStamp) + " seconds", 'relativePostition': relativePosition, 'imageBase64': frameAsBase64String})     # create frame json with collected metadata
        Utilities.exportJson(frameJson, self.topic_name_out)    # export frame json to kafka topic
        Utilities.storeJson(frameJson, "../../res/FramesMetadataETL/" + videoName + "_Metadata.txt")  # store frame json locally
        return


def main():
    """ Auto run main method """
    etl = VideoETL()
    etl.splitFrames()


if __name__ == "__main__":
    main()
    
