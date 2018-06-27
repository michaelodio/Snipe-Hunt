# Matt Stillwell
from kafka import KafkaProducer
import json


class Producer(object):

    @staticmethod
    def push_json(topic_name, data):
        """ Pushes JSON to topic within time interval """
        # Sets up the kafka producer to serialized json output on localhost port 9092
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        # blocks for syncronized sends: ensures message sent within 30 seconds
        timeout = 30
        producer.send(topic_name, data).get(timeout=timeout)

    @staticmethod
    def push_jsons(topic_name, json_array):
        """ Pushes array of JSONs to topic within time interval"""
        for json in json_array:
            Producer.push_json(topic_name, json)
