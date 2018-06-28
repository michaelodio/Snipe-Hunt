
import etl_tests
import kafka_consumer_tests
import kafka_producer_tests
import utility_tests


def test_all():
    """ Tests everything """
    etl_tests.test()
    kafka_consumer_tests.test()
    kafka_producer_tests.test()
    utility_tests.test()


def main():
    """ Auto run main method """
    test_all()


if __name__ == "__main__":
    main()
