# Matt Stillwell
from kafka import KafkaConsumer
import json
# listens on port 2181

class Consumer(object):

    @staticmethod
    def pull_jsons(topic_name):
        """ Listens on a topic for dictionaries """

        # Sets up the kafka consumer to listen for serialized json files on a specific topic
        consumer = KafkaConsumer(topic_name, value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                                 auto_offset_reset='earliest', enable_auto_commit=False)
        for message in consumer:
            data = message.value
            return data





