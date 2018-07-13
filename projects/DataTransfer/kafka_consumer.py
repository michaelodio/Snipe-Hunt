# Matt Stillwell
from kafka import KafkaConsumer
import json
# listens on port 2181


class Consumer(object):

    @staticmethod
    def initialize(topic_name):
        """ Initializes the consumer """
        # Sets up the kafka consumer to listen for serialized json files on a specific topic
        return KafkaConsumer(topic_name, value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 enable_auto_commit=False)
    

