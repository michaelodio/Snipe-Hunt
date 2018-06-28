import cv2
import json
import ntpath
import base64
import argparse
import sys
sys.path.insert(0, "../DataTransfer/")   # used to import files from other folder dir in project
sys.path.insert(0, "../ObjectDetection/")   # used to import files from other folder dir in project
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from kafka_manager import *
from TargettedObjectDetectionProcess import main as targetedObjDet
from utilities import *


class VideoETL(object):
    def __init__(self, videoPath):
        self.videoPath = videoPath
        self.videoName = ntpath.basename(self.videoPath)
        self.videoMetadataJson = None
        self.frameMetadataJsonList = []
        self.totalFrame = None
        self.FPS = None
        self.videoDuration = None

    def splitFrames(self):
        print("Splitting Frames and extracting metadata...\n")
        cap = cv2.VideoCapture(self.videoPath)    # open video in openCV
        self.totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # grab total frames in the video
        self.FPS = int(cap.get(cv2.CAP_PROP_FPS))     # grab the frames per second of the video
        self.videoDuration = round(self.totalFrame / self.FPS)   # calculate the video's duration
        self.videoMetadataJson = json.dumps({'videoPath': self.videoPath, 'videoName': self.videoName, 'videoDuration': str(self.videoDuration) + " seconds", 'totalFrames': self.totalFrame, 'FPS': self.FPS})  # convert metadata to json
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
        frameAsBase64String = base64.b64encode(frameConvertedToJPG)    # encode frame to base64String
        self.frameMetadataJsonList.append(json.dumps({'frameNum': frameNum, 'timeStamp': str(timeStamp) + " seconds", 'imageBase64': frameAsBase64String}))    # convert collected frame metadata to json and add it to list
        return

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()   # Parser to parse arguments passed
    parser.add_argument('--video', type=str, help='Path to video for processing')
    FLAGS, unparsed = parser.parse_known_args()
    if FLAGS.video:
        videoEditor = VideoETL(FLAGS.video)   # create instance of VideoEditor object for processing the video with OpenCV
        videoEditor.splitFrames()   # splits the frames of the video as well as runs the extractFrameMetadata method on that frame.
    file1 = open('../../res/videoJson.txt', 'w')   # open file handler for videoJson.txt
    file1.write(videoEditor.videoMetadataJson)     # write the metadata Json information on the video to the file
    Utilities.storeJson(videoEditor.frameMetadataJsonList, "../../res/frameMetadataListETL.txt")
    Utilities.exportJson(videoEditor.frameMetadataJsonList, "framefeeder")
    targetedObjDet()               # run targeted object detection script now that json files (frames) are pushed to kafka
          