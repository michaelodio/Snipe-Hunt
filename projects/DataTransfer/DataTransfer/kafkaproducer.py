# Matt Stillwell
from kafka import KafkaProducer
import json


class Producer(object):

    def __init__(self):
        """ Constructor: Sets up the kafka producer to serialized json output on localhost port 9092 """
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.timeout = 30    # blocks for syncronized sends: ensures message sent within 30 seconds

    def pushJSON(self, topic_name, json):
        """ Pushes JSON to topic within time interval """
        self.producer.send(topic_name, json).get(timeout=self.timeout)

    def pushJSONs(self, topic_name, json_array):
        """ Pushes array of JSONs to topic within time interval"""
        for json in json_array:
            self.pushJSON(topic_name, json)


def main():
    """ Main method: Creates instance of class and tests push method """
    topic_name = 'bay'
    data = [{"foo1": "bar"}, {"foo2": "bar"}, {"foo3": "bar"}]

    # {'filePath': 'PATH/TO/FILE', 'fileName': 'Flag.jpg'}

    p = Producer()
    p.pushJSONs(topic_name, data)


if __name__ == "__main__":
    main()
