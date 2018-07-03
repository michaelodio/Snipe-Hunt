./start_kafka_server.sh
wait
echo Kafka Server Started

./create_topic.sh general
./create_topic.sh target
./create_topic.sh framefeeder
echo Topics Created

cd ../projects/ObjectDetection/
python TargettedObjectDetectionProcess.py &

cd ../ETL/
python ETLProcess.py --video "../../res/bunny.mp4"

cd ../
./cleanup.py
echo Cleaned up files
