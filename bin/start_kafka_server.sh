cd ../res/Apps/kafka/

sudo bin/zookeeper-server-start.sh config/zookeeper.properties > bin/zookeeper-log.txt &
echo Zookeeper started

sudo bin/kafka-server-start.sh config/server.properties > bin/kafka-log.txt &
echo Kafka Server started
