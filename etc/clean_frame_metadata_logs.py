#!/usr/bin/python

import os
import glob


def remove(filePath):
    """ Removes a file given its path """
    files = glob.glob(filePath)
    for f in files:
        os.remove(f)


def main():
    """ Auto run main method """
    remove("../res/FramesMetadataGenObjDetections/*")
    remove("../res/FramesMetadataLabelingFrame/*")
    remove("../res/FramesMetadataTargetImgClassification/*")
    remove("../res/FramesMetadataETL/*")
    print("local metadata txt files deleted\n")


if __name__ == "__main__":
    main()
