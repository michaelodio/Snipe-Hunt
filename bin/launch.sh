./start_kafka_server.sh
wait
echo Kafka Server Started

./create_topic.sh general
./create_topic.sh target2
./create_topic.sh framefeeder
echo Topics Created

cd ../projects/ObjectDetection/
python FrameLabeling.py &

python GeneralObjDetection.py &

python TargettedObjectDetectionProcess.py &

cd ../ETL/
python ETLProcess.py --video "../../res/vid.mp4"

cd ../
./cleanup.py
echo Cleaned up files
