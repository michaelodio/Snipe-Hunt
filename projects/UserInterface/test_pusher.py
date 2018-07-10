import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


def main():
    import json
    # ETL correct
    # json_data = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    # "frameNum": 0.0, "timeStamp": "0.033 seconds", "imageBase64": "/9j/4j9k="}    
    
    # Target 
    # json_data4 = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    # "frameNum": 0.0, "timeStamp": "0.033 seconds", "foundTargetWithConfidence": "0.92655003", "imageBase64": "/9j/4j9k="}

    # General Obj correct
    
    json_data = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "imageBase64": "/9j/4j9k="}
    
    json_data2 = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "foundTargetWithConfidence": "0.92655003", "imageBase64": "/9j/4j9k="}

    # Label correct
    # json_data3 = {"LabeledImage": "GBURGBU"}
    
    jj = json.dumps(json_data)
    jj2 = json.dumps(json_data2)
    
    #"{\"name\": \"matt\", \"age\": \"20\"}"
    #json_data2 = "{\"name\": \"nick\", \"age\": \"21\"}"

    Utilities.exportJson(jj, "general")
    Utilities.exportJson(jj2, "general")
    #Utilities.exportJson(json_data2, "general")


if __name__=="__main__":
    main()

