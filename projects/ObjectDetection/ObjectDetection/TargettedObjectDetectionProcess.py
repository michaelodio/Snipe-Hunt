import subprocess





if __name__ == "__main__":
    graph = "/home/bt-intern2/TfModule/output_graph.pb"
    labels = "/home/bt-intern2/TfModule/output_labels.txt"
    input_layer = "Placeholder"
    output_layer = "Final_Result"
    input_height = 224
    input_width = 224
    frame = 0
    subprocess.call(("/home/bt-intern2/French-Flag-Finder/projects/ObjectDetection/ObjectDetection/label_image.py", graph),  shell=True)
