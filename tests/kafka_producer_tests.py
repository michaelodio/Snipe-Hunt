
import sys
sys.path.insert(0, '../projects/DataTransfer/')
from kafka_producer import *
    

def test_push_json():
    """ Tests the push_json method """
    topic_name = 'bay'
    data = {"frameNum": 0, "timeStamp": 0, "imageBase64": "32ff33ff32"}
    Producer.push_json(topic_name, data)


def test_push_jsons():
    """ Tests the push_jsons method """
    topic_name = 'bay'
    data = [{"frameNum": 1, "timeStamp": 10, "imageBase64": "234gr83hen"},
            {"frameNum": 2, "timeStamp": 20, "imageBase64": "43hfhuf6b3"},
            {"frameNum": 3, "timeStamp": 30, "imageBase64": "9fbufbh434"}]
    
    data2 = [{"frameNum": 4, "timeStamp": 40, "imageBase64": "7fgfb4w474"},
             {"frameNum": 5, "timeStamp": 50, "imageBase64": "1293948e43"},
             {"frameNum": 6, "timeStamp": 60, "imageBase64": "555405039k"}]
    
    Producer.push_jsons(topic_name, data)
    Producer.push_jsons(topic_name, data2)


def test():
    """ Runs all test methods for this class """
    test_push_json()
    test_push_jsons()


if __name__ == "__main__":
    test()
