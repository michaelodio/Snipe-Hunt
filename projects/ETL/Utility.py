import os
import cv2
import numpy
import glob
from os import walk
from os.path import splitext
from os.path import join
from Tkinter import *
from tkFileDialog import askopenfilename


class Utility(object):

    def __init__(self):
        """This is the constructor"""
        self.storePaths = []

    def get_file_paths(self, directory):
        extensions = [".mp4", ".mpg", ".mov", ".wmv"]
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(tuple(extensions)):
                    self.storePaths.append(os.path.join(root, f))

    def display_file_paths(self):
        for stuff in self.storePaths:
            print stuff

