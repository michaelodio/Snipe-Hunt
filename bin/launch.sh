./start_kafka_server.sh
wait
echo Kafka Server Started

./create_topic.sh general
./create_topic.sh target2
./create_topic.sh framefeeder
echo Topics Created
./clear_topic.sh general
./clear_topic.sh target2
./clear_topic.sh framefeeder
echo Topics Cleared

cd ../projects/ObjectDetection/
python FrameLabeling.py &

python GeneralObjDetection.py &

python TargettedObjectDetectionProcess.py --graph "../../res/TfModel/output_graph.pb" --labels "../../res/TfModel/output_labels.txt" --input_layer "Placeholder" --output_layer "final_result" --input_height 224 --input_width 224 &

cd ../ETL/
python ETLProcess.py --video "../../res/vid.mp4"


