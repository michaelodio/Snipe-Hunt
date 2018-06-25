from label_image import main as labelImage


if __name__ == "__main__":
    graph = "/home/bt-intern2/TfModule/output_graph.pb"
    labels = "/home/bt-intern2/TfModule/output_labels.txt"
    input_layer = "Placeholder"
    output_layer = "final_result"
    input_height = str(224)
    input_width = str(224)
    frame = "/home/bt-intern2/Downloads/TestImages/TestImagesCar/TestCar1.jpeg"
    labelImage(graph, labels, input_layer, output_layer, input_height, input_width, frame)
