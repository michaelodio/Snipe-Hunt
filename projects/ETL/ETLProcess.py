from __future__ import division
import ntpath
import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *

extensions = [".mp4", ".mpg", ".mov", ".wmv"]  # global variables for movie extensions

class VideoETL(object):
    def __init__(self, videoPath):
        self.videoPath = videoPath
        self.videoName = ntpath.basename(self.videoPath)
        self.totalFrame = None
        self.FPS = None
        self.videoDuration = None

    def splitFrames(self):
        print("Splitting Frames and extracting metadata...\n")
        cap = cv2.VideoCapture(self.videoPath)    # open video in openCV
        self.totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # grab total frames in the video
        self.FPS = int(cap.get(cv2.CAP_PROP_FPS))     # grab the frames per second of the video
        self.videoDuration = round(self.totalFrame / self.FPS)   # calculate the video's duration
        if cap.isOpened is False:
            print("Error opening video stream or file")
        for x in range(self.totalFrame):     # loop through all of the frames and extract meta data on each frame
            frameNum = cap.get(cv2.CAP_PROP_POS_FRAMES)
            retval, videoframe = cap.read()     # grab the next frame
            cv2.imencode(".jpeg", videoframe)    # convert frame to JPEG image.
            frame = cv2.resize(videoframe, (300,300))    # resize frame to 300x300
            self.extractFrameMetadata(frame, frameNum, cap)    # collect metadata on the frame
        cap.release()

    def extractFrameMetadata(self, frame, frameNum, cap):
        timeStamp = round(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000    # collect time stamp and convert it to seconds
        retval, frameConvertedToJPG = cv2.imencode('.jpg', frame)   # encode frame to .jpg for base64string conversion
        frameAsBase64String = Utilities.encodeFrame(frameConvertedToJPG)    # encode frame to base64String
        frameJson = json.dumps({'videoPath': self.videoPath, 'videoName': self.videoName, 'videoDuration': str(self.videoDuration) + " seconds", 'totalFrames': self.totalFrame, 'FPS': self.FPS, 'frameNum': frameNum, 'timeStamp': str(timeStamp) + " seconds", 'imageBase64': frameAsBase64String})     # create frame json with collected metadata
        Utilities.exportJson(frameJson, "framefeeder")    # export frame json to kafka topic
        Utilities.storeJson(frameJson, "../../res/FramesMetadataETL/FramesMetadata.txt")  # store frame json locally
        return

def main(*positional_parameters, **keyword_parameters):
    parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    parser.add_argument('--video', type=str, help='Path to video or folder of videos for processing')
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

          
        
        
if __name__ == "__main__":
    main()
    
