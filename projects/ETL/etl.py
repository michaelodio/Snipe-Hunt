import cv2

class VideoManager(object):

    def __init__(self, file_path):
        """Constructor- takes the file path of the video as a string for an argument"""
        self.file_path = file_path

    def split(self):
        """Splits the video into frames"""
        vidcap = cv2.VideoCapture(self.file_path)
        success, image = vidcap.read()
        count = 0
        success = True
        while success:
            cv2.imwrite("C:\\Users\\Matt\\Desktop\\Python\\French-Flag-Finder\\projects\\ETL\\res\\frames\\frame%d.jpg" % count, image)
            success, image = vidcap.read()
            #print('Read a new frame: ', success)
            count += 1

    def display(self):
        """Prints the file path of the video to the console"""
        #return self.file_path

def main():
    vm = VideoManager('C:\\Users\\Matt\\Desktop\\Python\\French-Flag-Finder\\projects\\ETL\\res\\bunny.mp4')
    vm.display()
    vm.split()
    
if __name__ == "__main__":
    main()