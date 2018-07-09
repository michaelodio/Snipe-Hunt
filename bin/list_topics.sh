#!/bin/sh

cd ../res/Apps/kafka/bin/

./kafka-topics.sh --zookeeper localhost:2181 \
                  --list
