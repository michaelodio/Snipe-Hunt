# Matt Stillwell
from nose.tools import *

import sys
sys.path.insert(0, '../projects/DataTransfer/')
from kafka_consumer import *


def test_pull_jsons():
    """ Tests the pull_jsons method """
    topic_name = "bay"
    Consumer.pull_jsons(topic_name)


def main():
    """ Auto run main method """
    test_pull_jsons()


if __name__ == "__main__":
    main()
