# Matt Stillwell
from kafka import KafkaConsumer
import json
# listens on port 2181


class Consumer(object):

    def __init__(self, topic_name):
        """ Constructor: Sets up the kafka consumer to listen for serialized json files on a specific topic """
        self.consumer = KafkaConsumer(topic_name, value_deserializer=lambda m: json.loads(m.decode('ascii')))
        # all:  auto_offset_reset='earliest', enable_auto_commit=False

    def pullJSONs(self):
        """ Listens on a topic for dictionaries """
        for message in self.consumer:
            print message.value


def main():
    """ Main method: Creates instance of class and tests pull method """
    topic_name = 'bay'
    c = Consumer(topic_name)
    c.pullJSONs()


if __name__ == "__main__":
    main()




