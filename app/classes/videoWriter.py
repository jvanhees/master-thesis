import numpy as np
import cv2
import math
import os.path

from video import VideoReader

class VideoWriter:
    
    def __init__(self, clip, folder):
        self.clip = clip
        self.folder = folder
        
        self.videoFile = clip.getVideoFile()
        
        self.reader = VideoReader(self.videoFile)
        self.frames = self.reader.getVideoFrames()
        
        self.fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
    
    # Create a video fragment from a clip
    def createVideo(self, start, end, filename):
        self.new(self.folder + filename, self.reader.width, self.reader.height, self.reader.fps)
        
        startFrame = int(start * self.reader.fps)
        endFrame = int(end * self.reader.fps)
        
        self.insertFrames(self.frames[startFrame:endFrame])
        self.writer.release()
        
    
    def new(self, filename, width, height, fps):
        self.writer = cv2.VideoWriter(filename + '.mp4', self.fourcc, int(fps), (int(width),int(height)))
    
    def insertFrames(self, frames):
        for idx, frame in enumerate(frames):
            self.writer.write(frame)
        
        print 'Done'