./start_kafka_server.sh
echo Kafka Server Started

./create_topic.sh general
./create_topic.sh target2
./create_topic.sh framefeeder
echo Topics Created

cd ../projects/ObjectDetection/
python TargettedObjectDetectionProcess.py &

cd ../ETL/
python ETLProcess.py --video "/home/bt-intern2/Iris/res/vid.mp4"
