import json
import csv
import os.path
import urllib

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



class Clip:
    
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
        
        if vidFolder == None:
            self.thumbFolder = 'data/thumbnails/'
        else:
            self.thumbFolder = thumbFolder
        
        
    
    def getClip(self):
        return self.clip
    
    
    def getClipId(self):
        return self.clipId    
    
    
    def getVideoFile(self):
        return self.vidFolder + self.clipId + '.mp4'
    
    
    # Returns relevant metadata
    def getMetadata(self):
        print self.clip
        ret = []
        if 'title' in self.clip:
            ret.append(self.clip['title'])
        if 'description' in self.clip:
            ret.append(self.clip['description'])
        if 'cat' in self.clip:
            ret.append(' '.join(self.clip['cat']))
        
        return ret
    
    
    # Returns relevant metadata as single text blob
    def getMetadataBlob(self):
        return ' '.join(self.getMetadata())
    
    
    def getThumbnail(self):
        if 'thumbnail' in self.clip:
            ext = os.path.splitext(self.clip['thumbnail']['sourcepath'])[1]
            fileName = self.thumbFolder + self.clipId + ext
            
            if os.path.isfile(fileName) == False:
                # Does not exist, so fetch it from online
                print "No thumbnail, fetching..."
                thumbnail = urllib.URLopener()
                # Gets 403 Forbidden
                thumbnail.retrieve('https://d2vt09yn8fcn7w.cloudfront.net/' + self.clip['thumbnail']['sourcepath'], fileName)
            
            return self.thumbFolder + self.clipId + '.jpg'
            
        else:
            return False