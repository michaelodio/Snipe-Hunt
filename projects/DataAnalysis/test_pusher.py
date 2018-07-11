import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


def main():
    
    label_json_data = {"LabeledImage": "GBURGBU", "videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "foundTargetWithConfidence": "0.92655003", "ObjectsDetected": ["Label: water bottle, 7.33%"], 
    "imageBase64": "/9j/4j9k="}
    
    jj = json.dumps(label_json_data)

    Utilities.exportJson(jj, "accumulo")


if __name__=="__main__":
    main()

