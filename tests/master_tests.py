
import etl_tests
import kafka_manager_tests
import kafka_consumer_tests
import kafka_producer_tests
import utility_tests

import sys
sys.path.insert(0, '../')
import cleanup


def test_all():
    """ Tests everything """
    print "\n=========================\n Running Tests\n========================="
    etl_tests.test()
    #kafka_manager_tests.test()
    kafka_producer_tests.test()
    kafka_consumer_tests.test()
    #utility_tests.test()
    
    clean()


def start_server():
    """ Starts kafka """
    import os
    os.system('cd ../bin/ && ./start_kafka_server.sh')
    print "\n-------------------------\n Kafka server started"


def clean():
    """ Runs the cleanup script """
    cleanup.run()
    print "\n\n Files Cleaned\n-------------------------"


def main():
    """ Auto run main method """
    start_server()
    test_all()


if __name__ == "__main__":
    main()
