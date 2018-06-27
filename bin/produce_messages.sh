echo $2 | ../res/Apps/kafka/bin/kafka-console-producer.sh --broker-list localhost:9092 --topic $1 > /dev/null
