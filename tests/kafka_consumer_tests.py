
import sys
sys.path.insert(0, '../projects/DataTransfer/')
from kafka_manager import *
    

def test_pull_jsons():
    """ Tests the pull_jsons method """
    topic_name = "bay"
    Consumer.pull_jsons(topic_name)


def test():
    """ Runs all test methods for this class """
    test_pull_jsons()
    print "    Kafka Consumer: Passed"


if __name__ == "__main__":
    test()
