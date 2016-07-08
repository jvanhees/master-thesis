import numpy as np
import cv2
import math
import os.path
from skimage import img_as_float

frames = 25

class VideoReader:
    
    def __init__(self, videoFile, cache=None):
        self.videoFile = videoFile
        
        if cache is None:
            self.cache = True
        else:
            self.cache = cache
        
        self.__tmpLocation = 'tmp/'
        
        self.cap = cv2.VideoCapture(videoFile)
        
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
        self.frames = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        self.width = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
        self.length = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        
        self.success, frame = self.cap.read()
        if self.success:
            self.channels = frame.shape[2]
    
    
    def __del__(self):
        self.closeVideo()
    
    # returns a numpy array of all frames in the video
    def getVideoFrames(self):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, 0)
        frames = []
        while(self.cap.isOpened()):
            success, frame = self.cap.read()
            if success==True:
                frames.append(frame)
            else:
                break
        
        self.cap.release()
        return np.array(frames)
    
    # Returns a single frame
    def getVideoFrame(self, frameNumber):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNumber)
        success, frame = self.cap.read()
        return frame
    
    # Returns a single frame that is prepared for caffe
    def getFrame(self, frameNumber):
        frame = self.getVideoFrame(frameNumber)
        return self.prepareForCaffe(frame)
    
    # Returns an array of frames prepared for use in Caffe
    def getFrames(self, interval, start=None, prepare=None):
        if start is None:
            start = 0
        
        if prepare is None:
            prepare = True
                    
        # Return empty array if we can't read video
        # if self.success is False:
        #     return False
        
        # Calculate number of frames that will be returned
        it = int(math.floor(self.frames / interval))
        frames = np.zeros((it, self.height, self.width, self.channels))
        
        for i in range(it):
            self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, i * interval)
            success, frame = self.cap.read()
            
            if success:
                if prepare:
                    frames[i] = self.prepareForCaffe(frame)
                else:
                    frames[i] = frame
        
        return frames
        
            
    def showFrame(self, frameNumber):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNumber)
        success, frame = self.cap.read()
        cv2.imshow('Frame',frame)
    
    def closeVideo(self):
        # Release everything if job is finished
        self.cap.release()
    
    def prepareForCaffe(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).astype('float') / 255