
import sys
sys.path.insert(0, '../projects/DataTransfer/')
import kafka_manager


def test_start_server():
    """ Tests the start_server method """
    kafka_manager.Manager.start_server()


def test_stop_server():
    """ Tests the stop_server method """
    kafka_manager.Manager.stop_server()


def test_create_topic():
    """ Tests the create_topic method """
    kafka_manager.Manager.create_topic('bay')


def test_clear_topic():
    """ Tests the clear_topic method """
    kafka_manager.Manager.clear_topic('bay')


def test_delete_topic():
    """ Tests the delete_topic method """
    kafka_manager.Manager.delete_topic('bay')


def test_describe_topic():
    """ Tests the describe_topic method """
    kafka_manager.Manager.describe_topic('bay')


def test_list_topics():
    """ Tests the list_topics method """
    kafka_manager.Manager.list_topics()


def test():
    """ Runs all test methods for this class """
    test_start_server()
    test_create_topic()
    test_describe_topic()
    test_clear_topic()
    test_list_topics()
    test_delete_topic()
    test_stop_server()
    
    print "    Kafka Manager: Passed"


if __name__ == "__main__":
    test()
