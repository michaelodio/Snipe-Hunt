import sys
sys.path.insert(0, "../Utility/")   # used to import files from other folder dir in project
from utilities import *


def main():
    import json
    '''
    # ETL correct
    etl_json_data = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "imageBase64": "/9j/4j9k="}    
    
    # Target 
    target_json_data = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "foundTargetWithConfidence": "0.92655003", "imageBase64": "/9j/4j9k="}

    # General Obj correct
    
    general_json_data = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "imageBase64": "/9j/4j9k="}
    
    gerneal_json_data2 = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "foundTargetWithConfidence": "0.92655003", "imageBase64": "/9j/4j9k="}

    # Label correct
    label_json_data = {"LabeledImage": "GBURGBU", "videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "imageBase64": "/9j/4j9k="}'''
    
    label_json_data = {"videoDuration": "8.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 2.0, "timeStamp": "0.099 seconds", "foundTargetWithConfidence": "0.99655003", "ObjectsDetected": ["Label: hook, 9.33%"], 
    "imageBase64": "/2fjifds="}
    
    label_json_data2 = {"videoDuration": "7.0 seconds", "videoName": "vid.mp4", "totalFrames": 206, "videoPath": "../../res/vid.mp4", "FPS": 29, 
    "frameNum": 0.0, "timeStamp": "0.033 seconds", "foundTargetWithConfidence": "0.92655003", "ObjectsDetected": ["Label: water bottle, 7.33%"], 
    "imageBase64": "/9j/4j9k="}

    
    
    jj = json.dumps(label_json_data)
    jj2 = json.dumps(label_json_data2)

    Utilities.exportJson(jj, "general")
    Utilities.exportJson(jj2, "general")


if __name__=="__main__":
    main()

