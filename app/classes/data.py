import json
import csv
import os.path
import urllib
import cv2

class DataProvider:
    
    datafile = 'data/clips.json'
    
    with open(datafile) as data_file:
        data = json.load(data_file)['items']
    
    def getClip(self, clipId):
        for clip in self.data:
            if clip['id'] == clipId:
                return clip
        
        return False
    
    def getClips(self):
        return self.data