./start_kafka_server.sh
echo Kafka Server Started

./create_topic.sh general
./create_topic.sh target
./create_topic.sh framefeeder
echo Topics Created

cd ../projects/ObjectDetection/
python TargettedObjectDetectionProcess.py

cd ../projects/ETL/
python ETLProcess.py