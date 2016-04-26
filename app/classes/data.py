import json

class DataProvider:

    def __init__(self, datafile=None):
        if datafile == None:
            self.datafile = 'data/data.json'
        
        self.data = self.__loadData()
    
    
    def __loadData(self):
        with open(self.datafile) as data_file:
            return json.load(data_file)['items']
    
    
    def getClip(self, clipId):
        for clip in self.data:
            if clip['id'] == clipId:
                return clip
        
        return False
    
    def getClips(self):
        return self.data



class Clip:
    
    def __init__(self, clip=None, vidFolder=None):
        if clip != None:
            # Clip is not none, assume clip object
            self.clipId = clip['id']
            self.clip = clip
        else:
            raise NameError('No clip(id) supplied')
        
        if vidFolder == None:
            self.vidFolder = 'data/video/'
    
    
    def getClip(self):
        return self.clip
    
    
    def getClipId(self):
        return self.clipId    
    
    
    def getVideoFile(self):
        return self.vidFolder + self.clipId + '.mp4'
    
    
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
    
    
    # Returns relevant metadata as single text blob
    def getMetadataBlob(self):
        return ' '.join(self.getMetadata())