#!/bin/sh


cd ../etc/
python clean_frame_metadata_logs.py

cd ../bin
./start_kafka_server.sh
wait

cd ../etc/
python clean_and_clear_topics.py

# ======================================================================
#                             DATABASE
# ======================================================================

#cd ../projects/DataStorage/
#python ToAccumulo.py --topic_name_in "Accumulo" &

#gnome-terminal -e "tail -f -n 0 ../../logs/shipToAccumulo.log" &



# ======================================================================
#                          FRAME LABELING
# ======================================================================

cd ../projects/ObjectDetection/
python FrameLabeling.py --model "../../res/MobileNetSSD_deploy.caffemodel" \
                        --model_prototxt "../../res/MobileNetSSD_deploy.prototxt.txt" \
                        --labels "../../res/labels.txt" \
                        --topic_name_in "general" \
                        --topic_name_out "Accumulo" &

gnome-terminal -e 'bash -c "printf \"\e]2;Frame Labeling\a\" && 
                   tail -f -n 0 ../../logs/FrameLabeling.log; exec bash"' &



# ======================================================================
#                     GENERAL OBJECT DETECTION
# ======================================================================

python GeneralObjDetection.py --model "../../res/MobileNetSSD_deploy.caffemodel" \
                              --model_prototxt "../../res/MobileNetSSD_deploy.prototxt.txt" \
                              --labels "../../res/labels.txt" \
                              --topic_name_in "target2" \
                              --topic_name_out "general" &

#python GeneralObjDetectionYOLO.py --net "cfg/yolov3-tiny.cfg" \
                                  #--weights "yolov3-tiny.weights" \
                                  #--meta "cfg/coco.data" \
                                  #--topic_name_in "target2" \
                                  #--topic_name_out "general" &
                                  
gnome-terminal -e 'bash -c "printf \"\e]2;General Object Detection\a\" && 
                   tail -f -n 0 ../../logs/GeneralObjectDetection.log; exec bash"' &



# ======================================================================
#                    TARGETED OBJECT DETECTION
# ======================================================================

python TargettedObjectDetectionProcess.py --graph "../../res/TfModel/output_graph.pb" \
                                          --labels "../../res/TfModel/output_labels.txt" \
                                          --input_layer "Placeholder" \
                                          --output_layer "final_result" \
                                          --input_height 224 \
                                          --input_width 224 \
                                          --topic_name_in "framefeeder" \
                                          --topic_name_out "target2" &

gnome-terminal -e 'bash -c "printf \"\e]2;Targetted Object Detection\a\" && 
                   tail -f -n 0 ../../logs/TargettedObjectDetection.log; exec bash"' &


# ======================================================================
#                             ETL
# ======================================================================

cd ../ETL/
python ETLProcess.py --topic_name_in "pathfinder" \
                     --topic_name_out "framefeeder" &

gnome-terminal -e 'bash -c "printf \"\e]2;ETL\a\" && 
                   tail -f -n 0 ../../logs/ETL.log; exec bash"' &


# ======================================================================
#                          PATH PASSER
# ======================================================================

cd ../Utility/
inotifywait -m /home/smoke-admin/Desktop/tomcat9/webapps/Witch-Hunt/res/ -e create -e moved_to |
    while read path action file; do
        python path_passer.py --video_path $path$file \
                             --topic_name_out "pathfinder" &
    done




#cd ../../etc/
#python clean-pyc.py
