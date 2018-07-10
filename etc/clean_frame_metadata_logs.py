#!/usr/bin/python

import os


def remove(file):
    """ Removes a file given its path """
    ## If file exists, delete it ##
    if os.path.isfile(file):
        os.remove(file)
        print("Removed %s" % file)
    else:    ## Show an error ##
        print("Error: %s file not found" % file)


def main():
    """ Auto run main method """
    remove("../res/FramesMetadataGenObjDetections/framesMetadata.txt")
    remove("../res/FramesMetadataLabelingFrame/frameMetadata.txt")
    remove("../res/FramesMetadataTargetImgClassification/frameMetadata.txt")
    remove("../res/FramesMetadataETL/FramesMetadata.txt")


if __name__ == "__main__":
    main()
