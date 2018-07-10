#!/bin/sh

cd ../res/Apps/kafka/

sudo bin/zookeeper-server-stop.sh > bin/zookeeper-log.txt &
echo Zookeeper stopped

sudo bin/kafka-server-stop.sh > bin/kafka-log.txt &
echo Kafka Server stopped
