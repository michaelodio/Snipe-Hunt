# Matt Stillwell
from kafka import KafkaConsumer
# listens on port 2181


class Consumer(object):

    @staticmethod
    def pull_jsons(topic_name):
        """ Listens on a topic for dictionaries """
        import json
        # Sets up the kafka consumer to listen for serialized json files on a specific topic
        consumer = KafkaConsumer(topic_name, value_deserializer=lambda m: json.loads(m.decode('ascii')))
        # all:  auto_offset_reset='earliest', enable_auto_commit=False
        print "------------------------------\nFrame#\tTime\tImage\n------------------------------"
        for message in consumer:
            data = message.value
            print "%r\t\t%r\t\t%r" % (get_frame_num(data),
                                  get_time_stamp(data),
                                  get_image_base_64(data))


def get_frame_num(data):
    """ Returns frame number from json """
    return data['frameNum']


def get_time_stamp(data):
    """ Returns time stamp from json """
    return data['timeStamp']


def get_image_base_64(data):
    """ Returns image base 64 from json """
    return data['imageBase64'].encode("ascii")


def main():
    """ Main method: Creates instance of class and tests pull method """
    topic_name = 'bay'
    c = Consumer(topic_name)
    c.pull_jsons()


if __name__ == "__main__":
    main()




