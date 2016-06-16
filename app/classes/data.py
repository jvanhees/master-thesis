import json
import csv
import os.path
import urllib
import cv2

from clip import Clip

class DataProvider:

    datafile = 'data/clips.json'
    with open(datafile) as data_file:
        data = json.load(data_file)['items']
    
    def __init__(self):
        self.videoFolder = '/Volumes/Jorick van Hees/video-data/files/'
    
    
    def getClip(self, clipId):
        for clip in self.data:
            if clip['id'] == clipId:
                return Clip(clip, self.videoFolder)
        
        return False
    
    def getClips(self):
        clips = []
        
        for idx, clip in enumerate(self.data):
            clips.append(Clip(clip, self.videoFolder))
            
        return clips