import json
import csv
import os.path
import urllib
import cv2

from classes.clip import Clip

datafile = 'data/clean.json'
with open(datafile) as data_file:
    data = json.load(data_file)
    
videoFolder = '/Volumes/Jorick van Hees/video-data/files/'


print len(data)
for idx, c in enumerate(data):
    clip = Clip(c, videoFolder)
    
    if not clip.hasVideo():
        del data[idx]
        print 'No video ('+clip.clipId+')'
        continue
    
    if len(clip.getMetadataBlob()) == 0:
        del data[idx]
        print 'No metadata ('+clip.clipId+')'
        continue
    
print len(data)
with open('data/clean.json', 'w') as outfile:
    json.dump(data, outfile)