import cv2
import json
import ntpath
import base64
import argparse
import sys
from os.path import expanduser
sys.path.insert(0, expanduser("~") + "/French-Flag-Finder/projects/DataTransfer/DataTransfer/")   # used to import files from other folder dir in project
sys.path.insert(0, expanduser("~") + "/French-Flag-Finder/projects/ObjectDetection/ObjectDetection")   # used to import files from other folder dir in project
from kafka_manager import *
from TargettedObjectDetectionProcess import main as targetedObjDet


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

    def storeJson(self):
        print("Storing metadata Json files locally... \n")
        file1 = open('/home/bt-intern2/French-Flag-Finder/projects/ETL/ETL/videoJson.txt', 'w')   # open file handler for videoJson.txt
        file2 = open('/home/bt-intern2/French-Flag-Finder/projects/ETL/ETL/framesJson.txt', 'w')   # open file handler for framesJson.txt
        file1.write(self.videoMetadataJson)     # write the metadata Json information on the video to the file
        for i in range(len(self.frameMetadataJsonList)):     # loop through the list of the frames metadata Jsons and write them to the the file
            file2.write(str(self.frameMetadataJsonList[i]) + "\n\n")
        file1.close()
        file2.close()
        
    def exportJsons(self):
        print("Exporting Json files to kafka topic 'framefeeder'")
        for i in range(len(self.frameMetadataJsonList)/10):
            print("Exporting frame " + str(i))
            Producer.push_json("framefeeder", self.frameMetadataJsonList[i])
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=str, help='Path to video for processing')
    FLAGS, unparsed = parser.parse_known_args()
    if FLAGS.video:
        videoEditor = VideoETL(FLAGS.video)
        videoEditor.splitFrames()   # splits the frames of the video as well as runs the extractFrameMetadata method on that frame.
        videoEditor.storeJson()    # stores the Json files locally
        videoEditor.exportJsons()  # push json files to kafka topic 'framefeeder'
    targetedObjDet()               # run targeted object detection script now that json files (frames) are pushed to kafka
          