
import sys
sys.path.insert(0, '../projects/DataTransfer/')
from kafka_consumer import *


def test_pull_jsons():
    """ Tests the pull_jsons method """
    topic_name = "bay"
    consumer = Consumer.initialize(topic_name)
    for m in consumer:
            json_data = m.value 
            print json_data
    consumer.close()


def test():
    """ Runs all test methods for this class """
    test_pull_jsons()


if __name__ == "__main__":
    test()
