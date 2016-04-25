import numpy as np
import cv2
import math
from skimage import img_as_float

frames = 25

class Video:
    
    def __init__(self, videoFile):
        self.cap = cv2.VideoCapture(videoFile)
        
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
        self.frames = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        self.width = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        
        success, frame = self.cap.read()
        if success:
            self.channels = frame.shape[2]
        else:
            return false
        
    # Returns a single frame that is prepared for caffe
    def getFrame(self, frameNumber):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNumber)
        success, frame = self.cap.read()
        if success:
            return self.prepareForCaffe(frame)
        else:
            return False
    
    # Returns an array of frames prepared for use in Caffe
    def getFrames(self, interval, start=None):
        if start is None:
            start = 0
        
        # Calculate number of frames that will be returned
        it = int(math.floor(self.frames / interval))
        frames = np.zeros((it, self.height, self.width, self.channels))
        
        for i in range(it):
            self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i * interval)
            success, frame = self.cap.read()
            
            if success:
                frames[i] = self.prepareForCaffe(frame)
        
        return frames
        
            
    def showFrame(self, frame):
        cv2.imshow('Frame',frame)
    
    def closeVideo(self):
        # Release everything if job is finished
        self.cap.release()
    
    def prepareForCaffe(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype('float') / 255