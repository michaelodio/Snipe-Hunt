# Matt Stillwell
from kafka import KafkaProducer
import json


class Producer(object):

    def __init__(self):
        """ Constructor: Sets up the kafka producer to serialized json output on localhost port 9092 """
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.timeout = 30    # blocks for syncronized sends: ensures message sent within 30 seconds

    def push_json(self, topic_name, json):
        """ Pushes JSON to topic within time interval """
        self.producer.send(topic_name, json).get(timeout=self.timeout)

    def push_jsons(self, topic_name, json_array):
        """ Pushes array of JSONs to topic within time interval"""
        for json in json_array:
            self.push_json(topic_name, json)


def main():
    """ Main method: Creates instance of class and tests push method """
    topic_name = 'bay'
    data = [{"frameNum": 1, "timeStamp": 10, "imageBase64": "234gr83hen"},
            {"frameNum": 2, "timeStamp": 20, "imageBase64": "43hfhuf6b3"},
            {"frameNum": 3, "timeStamp": 30, "imageBase64": "9fbufbh434"}]

    data2 = [{"frameNum": 4, "timeStamp": 40, "imageBase64": "7fgfb4w474"},
             {"frameNum": 5, "timeStamp": 50, "imageBase64": "1293948e43"},
             {"frameNum": 6, "timeStamp": 60, "imageBase64": "555405039k"}]

    p = Producer()
    #p.push_jsons(topic_name, data)
    p.push_jsons(topic_name, data2)


if __name__ == "__main__":
    main()
