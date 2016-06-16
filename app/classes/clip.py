import json
import csv
import urllib
import cv2
import numpy as np
import sys
import os.path

from video import VideoReader
from caffenet import CaffeNet

class Clip:
    
    # Init caffenet for evaluation
    net = CaffeNet()
    
    def __init__(self, clip=None, vidFolder=None, thumbFolder=None):
        if clip != None:
            self.clipId = clip['id']
            self.clip = clip
        else:
            raise NameError('No clip(id) supplied')
        
        if vidFolder == None:
            self.vidFolder = 'data/videos/'
        else:
            self.vidFolder = vidFolder
        
        if thumbFolder == None:
            self.thumbFolder = 'data/thumbnails/'
        else:
            self.thumbFolder = thumbFolder
        
        self.interval = 25
        self.start = 0
        self.__tmpLocation = 'tmp/'
        
        self.cache = True
        self.concepts = None
        
    
    def hasVideo(self):
        self.videoReader = VideoReader(self.getVideoFile())
        return self.videoReader.success
    
    def getClip(self):
        return self.clip
    
    
    def getClipId(self):
        return self.clipId    
    
    
    def getVideoFile(self):
        return self.vidFolder + self.clipId + '.mp4'
    
    
    def getFrames(self):
        self.videoReader = VideoReader(self.getVideoFile())
        return self.videoReader.getFrames(self.interval, self.start)
            
    
    def getConcepts(self, start=None, end=None, indexes=None):        
        fileName = self.__tmpLocation + self.clipId + '_' + str(self.interval) + '.concepts.npy'
        # Check if a file with concepts with this interval already exists
        if self.concepts == None:
            try:
                self.concepts = np.load(fileName)
            except (IOError):
                # No file found, so get concepts and save them
                frames = self.getFrames()
                self.concepts = self.net.classify(frames)
                np.save(fileName, self.concepts)
        
        if start != None and end != None and indexes == None:
            return self.concepts[start:end]
        
        if indexes != None:
            return np.take(self.concepts, indexes, axis=0)
            
        return self.concepts
    
    
    # Get concepts for mediaclip thumbnail image with caffenet
    def getThumbnailConcepts(self):
        thumbnail = self.getThumbnail()
        
        if thumbnail != False:
            frame = self.net.loadImage(thumbnail)
            return self.net.classify([frame])[0]
        else:
            return False
            
    
    # Returns relevant metadata
    def getMetadata(self):
        ret = []
        if 'title' in self.clip:
            ret.append(self.clip['title'])
        if 'description' in self.clip:
            ret.append(self.clip['description'])
        if 'cat' in self.clip:
            ret.append(' '.join(self.clip['cat']))
        
        return ret
    
    
    # Returns clip title
    def getTitle(self):
        if 'title' in self.clip:
            return self.clip['title']
        else:
            return 'n/a'
        
        
    # Returns relevant metadata as single text blob
    def getMetadataBlob(self):
        return ' '.join(self.getMetadata())
    
    
    def getThumbnailFrame(self):
        thumbnailUrl = self.getThumbnail()
        
        if thumbnailUrl:
            return cv2.imread(thumbnailUrl, flags=cv2.IMREAD_COLOR)
        else:
            return False
        
    
    def getThumbnail(self):
        if 'thumbnail' in self.clip:
            ext = os.path.splitext(self.clip['thumbnail']['sourcepath'])[1]
            fileName = str(self.thumbFolder) + str(self.clipId) + str(ext)
            
            if os.path.isfile(fileName) == False:
                # Does not exist, so fetch it from online
                self._downloadThumbnail(fileName)
            
            return str(self.thumbFolder) + str(self.clipId) + '.jpg'
            
        else:
            return False
    
    
    def createVideoFragment(self, startTime, length):
        self.videoReader.createVideo(startTime, length, str(self.clipId), 'output/')
        
    
    def setInterval(self, interval):
        self.interval = int(interval)
    
    def setStart(self, start):
        self.start = int(start)
    
    def setCache(self, cache):
        self.cache = bool(cache)
    
    def _downloadThumbnail(self, fileName):
        thumbnail = urllib.URLopener()
        # Cloudfront: Gets 403 Forbidden
        # url = 'https://d2vt09yn8fcn7w.cloudfront.net' + self.clip['thumbnail']['sourcepath']
        # pthumbnail:
        url = 'http://landmark.bbvms.com/mediaclip/' + self.clipId + '/pthumbnail/default/default.jpg'
        
        print url
        thumbnail.retrieve(url, fileName)