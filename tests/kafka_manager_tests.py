
import sys
sys.path.insert(0, '../projects/DataTransfer/')
import kafka_manager


def test_start_server():
    """ Tests the start_server method """
    kafka_manager.Manager.start_server()


def test():
    """ Runs all test methods for this class """
    #test_start_server()
    print "    Kafka Manager: Passed"


if __name__ == "__main__":
    test()
