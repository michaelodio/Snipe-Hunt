import cv2

class VideoManager(object):

    def __init__(self, file_path):
        """Constructor- takes the file path of the video as a string for an argument"""
        self.file_path = file_path

    def split(self):
        """Splits the video into frames"""
        print "hello"
        vidcap = cv2.VideoCapture(self.file_path)
        success, image = vidcap.read()
        count = 0
        success = True
        while success:
            cv2.imwrite("frame%d.jpg" % count, image)
            success, image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1
        print "hi"

    def display(self):
        """Prints the file path of the video to the console"""
        print self.file_path
