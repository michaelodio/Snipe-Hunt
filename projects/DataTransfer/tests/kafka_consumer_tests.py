# Matt Stillwell
from DataTransfer.DataTransfer.kafka_consumer import *


def test_pull_jsons():
    """ Tests the pull_jsons method """
    topic_name = "bay"
    consumer = Consumer(topic_name)
    consumer.pull_jsons()


def test_get_num_frame():
    """ Tests the get_num_frame method """
    data = {"frameNum": 13, "timeStamp": 0, "imageBase64": "32ff33ff32"}
    get_frame_num(data)


def test_get_time_stamp():
    """ Tests the get_time_stamp method """
    data = {"frameNum": 13, "timeStamp": 0, "imageBase64": "32ff33ff32"}
    get_time_stamp(data)


def test_get_image_base_64():
    """ Tests the get_image_base_64 method """
    data = {"frameNum": 13, "timeStamp": 0, "imageBase64": "32ff33ff32"}
    get_image_base_64(data)

