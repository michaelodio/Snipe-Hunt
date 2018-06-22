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
        print "------------------------------\nFrame#\tTime\tImage\n------------------------------"
        for message in consumer:
            data = message.value
            print "%r\t\t%r\t\t%r" % (Consumer.get_frame_num(data),
                                      Consumer.get_time_stamp(data),
                                      Consumer.get_image_base_64(data))

    @staticmethod
    def get_frame_num(data):
        """ Returns frame number from json """
        return int(data['frameNum'])

    @staticmethod
    def get_time_stamp(data):
        """ Returns time stamp from json """
        return int(data['timeStamp'])

    @staticmethod
    def get_image_base_64(data):
        """ Returns image base 64 from json """
        return data['imageBase64'].encode("ascii")



