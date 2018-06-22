# Matt Stillwell
from kafka import KafkaConsumer
import json
# listens on port 2181


class Consumer(object):

    def __init__(self, topic_name):
        """ Constructor: Sets up the kafka consumer to listen for serialized json files on a specific topic """
        self.consumer = KafkaConsumer(topic_name, value_deserializer=lambda m: json.loads(m.decode('ascii')))
        # all:  auto_offset_reset='earliest', enable_auto_commit=False

    def pull_jsons(self):
        """ Listens on a topic for dictionaries """
        print "------------------------------\nFrame#\tTime\tImage\n------------------------------"
        for message in self.consumer:
            json = message.value
            print "%r\t\t%r\t\t%r" % (get_frame_num(json),
                                  get_time_stamp(json),
                                  get_image_base_64(json))


def get_frame_num(json):
    """ Returns frame number from json """
    return json['frameNum']


def get_time_stamp(json):
    """ Returns time stamp from json """
    return json['timeStamp']


def get_image_base_64(json):
    """ Returns image base 64 from json """
    return json['imageBase64'].encode("ascii")


def main():
    """ Main method: Creates instance of class and tests pull method """
    topic_name = 'bay'
    c = Consumer(topic_name)
    c.pull_jsons()


if __name__ == "__main__":
    main()




