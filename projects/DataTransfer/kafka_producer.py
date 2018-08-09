# Matt Stillwell
from kafka import KafkaProducer
import json


class Producer(object):

    @staticmethod
    def initialize():
        """ Initializes the producer """
        # Sets up the kafka producer to serialized json output on localhost port 9092
        return KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'), max_request_size='15000000')


def push_json(producer, topic_name, data):
    """ Pushes JSON to topic within time interval """
    # blocks for syncronized sends: ensures message sent within 30 seconds
    producer.send(topic_name, data).get(timeout=30)


def push_jsons(producer, topic_name, json_array):
    """ Pushes array of JSONs to topic within time interval"""
    for json in json_array:
        push_json(producer, topic_name, json)
