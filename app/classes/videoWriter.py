import numpy as np
import cv2
import math
import os.path

frames = 25

class VideoWriter:
    
    def __init__(self):
        
        
    
    def new(self, filename, width, height, fps):
        fourcc = cv2.cv.CV_FOURCC(*'MP4V')
        self.videoWriter = cv2.VideoWriter(filename, fourcc, fps, (width,height))
    
    def frame(self, frame):
        