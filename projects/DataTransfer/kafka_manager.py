from kafka_consumer import *
from kafka_producer import *


class Manager:

    @staticmethod
    def start_server():
        """ Starts kafka """
        import os
        os.system('cd ../../bin/ && ./start_server.sh')

    @staticmethod
    def stop_server():
        """ Stops kafka """
        import os
        os.system('cd ../../bin/ && ./stop_server.sh')

    @staticmethod
    def clear_topic(topic_name):
        """ Clears the topic """
        import os
        str = 'cd ../../bin/ && ./clear_topic.sh %s' % topic_name
        os.system(str)

    @staticmethod
    def delete_topic(topic_name):
        """ Deletes the topic """
        import os
        str = 'cd ../../bin/ && ./delete_topic.sh %s' % topic_name
        os.system(str)

    @staticmethod
    def describe_topic(topic_name):
        """ Describes the topic """
        import os
        str = 'cd ../../bin/ && ./describe_topic.sh %s' % topic_name
        os.system(str)

    @staticmethod
    def list_topics():
        """ Lists the topics """
        import os
        os.system('cd ../../bin/ && ./list_topics.sh')
