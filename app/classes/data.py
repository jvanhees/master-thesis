import json
import csv
import os.path
import urllib
import cv2

from clip import Clip

class DataProvider:

    datafile = 'data/clean.json'
    with open(datafile) as data_file:
        data = json.load(data_file)
    
    def __init__(self):
        self.videoFolder = '/Volumes/Jorick van Hees/video-data/files/'
    
    
    def getClip(self, clipId):
        for clip in self.data:
            if int(clip['id']) == int(clipId):
                return Clip(clip, self.videoFolder)
        
        return False
    
    def getClips(self):
        clips = []
        
        for idx, clip in enumerate(self.data):
            clips.append(Clip(clip, self.videoFolder))
            
        return clips