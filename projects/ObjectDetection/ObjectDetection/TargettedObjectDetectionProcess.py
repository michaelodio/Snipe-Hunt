from label_image import main as labelImage
import cv2

graph = "/home/bt-intern2/TfModule/output_graph.pb"
labels = "/home/bt-intern2/TfModule/output_labels.txt"
input_layer = "Placeholder"
output_layer = "final_result"
input_height = 224
input_width = 224
frame = "/home/bt-intern2/Downloads/TestImages/TestImagesCar/TestCar1.jpeg"
video = "/home/bt-intern2/Videos/French Flag Presented by Army Football Team.mp4"

if __name__ == "__main__":
    cap = cv2.VideoCapture(video)    # open video in openCV
    totalFrame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # grab total frames in the video
    for x in range(totalFrame):     # loop through all of the frames and run label_image.py script against the frames to see if the french flag is present
        retval, frame = cap.read()     # grab the next frame
        framePath = "/home/bt-intern2/Pictures/ObjectDetection/frame" + str(x) + ".jpeg"
        cv2.imwrite(framePath, frame)
        print("frame " + str(x) + ":")
        labelImage(graph, labels, input_layer, output_layer, input_height, input_width, framePath)
