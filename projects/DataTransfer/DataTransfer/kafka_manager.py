from kafka_consumer import *
from kafka_producer import *


class Manager:

    @staticmethod
    def start_server():
        """ Starts kafka """
        import os
        os.system('./start_server.sh')

    @staticmethod
    def stop_server():
        """ Starts kafka """
        import os
        os.system('./stop_server.sh')

    @staticmethod
    def clear_topic(topic_name):
        """ Clears the topic """
        import os
        str = './clear_topic.sh %s' % topic_name
        os.system(str)

    @staticmethod
    def list_topics():
        """ Lists the topics """
        import os
        os.system('./list_topics.sh')
