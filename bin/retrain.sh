#!/bin/sh

cd ../res/TfModel/
python retrain.py --image_dir ~/Pictures/trainingfolder \
                  --tfhub_module https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/2 \
                  --how_many_training_steps 1000 \
                  --train_batch_size 100 \
                  --learning_rate 0.1 \
                  --output_graph ../TfModel/output_graph.pb \
                  --output_labels ../TfModel/output_labels.txt

