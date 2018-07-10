#!/usr/bin/python

import os
from subprocess_manager import *

'''
cd ../bin
./start_kafka_server.sh
wait

./create_topic.sh general
./create_topic.sh target2
./create_topic.sh framefeeder
echo Topics Created

./clear_topic.sh general
./clear_topic.sh target2
./clear_topic.sh framefeeder
echo Topics Cleared
'''

def topic_exists(topic_name):
    output = get_bash("./list_topics.sh", directory="../bin/")
    outputarray = parse_output(output)
    for topic in outputarray:
        if topic == topic_name:
            return True
    return False


def parse_output(outputstr):
    return outputstr.split()


def clean_clear(topic_name):
    if topic_exists(topic_name):
        command = "./clear_topic.sh %s" % topic_name
        bash(command, directory="../bin/")
    else:
        command = "./create_topic.sh %s" % topic_name
        bash(command, directory="../bin/")


def main():
    """ Auto run main method """
    clean_clear("general")
    clean_clear("target2")
    clean_clear("framefeeder")
    print "Topics cleaned and cleared"


if __name__ == "__main__":
    main()
