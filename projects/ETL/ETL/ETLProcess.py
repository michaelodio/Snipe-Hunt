import cv2
import json
import ntpath
import base64



class VideoETL(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileName = ntpath.basename(self.filePath)
        self.frameList = []
        self.frameMetadataDictList = []
        self.videoMetadataDict = {}
        self.videoMetadataJson = None
        self.frameMetadataJsonList = []
        self.totalFrame = None
        self.FPS = None



    def splitFrames(self):
        print("Splitting Frames...\n")
        cap = cv2.VideoCapture(self.filePath)    # open video in openCV
        # collect metadata on video as a whole
        self.totalFrame = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))    # grab total frames in the video
        self.FPS = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))     # grab the frames per second of the video
        self.videoMetadataDict = {'filePath': self.filePath, 'fileName': self.fileName, 'totalFrames': self.totalFrame, 'FPS': self.FPS}    # store collected metadata of the video as a dict
        # if video cap(ture) is open then start loop for splitting frames and extracting metadata on each frame.
        if cap.isOpened is False:
            print("Error opening video stream or file")
        for x in range(self.totalFrame):     # loop through all of the frames and add the frames to a list and extract meta data on each frame
            frameNum = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
            retval, frame = cap.read()     # grab the next frame
            self.frameList.append(frame)    # add the frame to a list
            self.extractFrameMetadata(frame, frameNum, cap)    # collect metadata on the frame
        cap.release()

    def extractFrameMetadata(self, frame, frameNum, cap):
        timeStamp = round(cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)) / 1000    # collect time stamp and convert it to seconds
        retval, frameConvertedToJPG = cv2.imencode('.jpg', frame)   # encode frame to .jpg for base64string conversion
        frameAsBase64String = base64.b64encode(frameConvertedToJPG)    # encode frame to base64String
        self.frameMetadataDictList.append({'frameNum': frameNum, 'timeStamp': str(timeStamp) + " seconds", 'imageBase64': frameAsBase64String})    # add collected frame metadata to list
        return

    def createJson(self):
        self.videoMetadataJson = json.dumps(self.videoMetadataDict)    # creates a JSON string of the video metadata python dictionary
        print("Video metadata converted to Json: " + self.videoMetadataJson + "\n")
        print("Each frame's metadata converted to Json: ")
        for i in range(len(self.frameMetadataDictList)):
            frameMetadataDictToJson = json.dumps(self.frameMetadataDictList[i])    # creates a JSON string of the metadata of a certain frame from a python dictionary
            self.frameMetadataJsonList.append(frameMetadataDictToJson)    # adds the JSON string of that certain frame to a list



def main():
    videoEditor = VideoETL("/home/bt-intern5/Videos/Nature Beautiful short video 720p HD.mp4")  # creates a videoETL object that can perform the ETL methods on a video
    videoEditor.splitFrames()   # splits the frames of the video as well as runs the extractFrameMetadata method on that frame.
    videoEditor.createJson()   # creates and stores a JSON of the video metadata and JSONS of each frame's metadata.
    return


if __name__ == "__main__":
    main()

