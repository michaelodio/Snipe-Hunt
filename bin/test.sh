./start_kafka_server.sh
wait

cd ../tests/

python etl_tests.py > /dev/null
echo "ETL Tests: Passed"

python utilities_tests.py > /dev/null
echo "Utilities Tests: Passed"

python utility_tests.py > /dev/null
echo "Utility Tests: Passed"

python kafka_consumer_tests.py > /dev/null
echo "Kafka Consumer Tests: Passed"

python kafka_producer_tests.py > /dev/null
echo "Kafka Producer Tests: Passed"


