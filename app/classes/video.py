import numpy as np
import cv2

frames = 25

class Video:
    
    def __init__(self, videoFile):
        self.cap = cv2.VideoCapture(videoFile)
        
        self.fps = self.cap.get(cv2.cv.CV_CAP_PROP_FPS)
        self.frames = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        self.width = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

    def getFrame(self, frameNumber):
        self.cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNumber)
        success, frame = self.cap.read()
        if success:
            return self.convertToRGB(frame)
        else:
            return False
            
    def showFrame(self, frame):
        cv2.imshow('Frame',frame)
    
    def closeVideo(self):
        # Release everything if job is finished
        self.cap.release()
    
    def convertToRGB(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)