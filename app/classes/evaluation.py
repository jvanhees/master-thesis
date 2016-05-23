import numpy as np
import cv2
import warnings
from scipy import spatial

from caffenet import CaffeNet
from video import Video
from data import Clip


frames = 25

# Evaluate frames for a specific clip.
class Evaluate:
    
    # Init caffenet for evaluation
    net = CaffeNet()
    
    def __init__(self, clip):
        print "Starting evaluation for clip " + clip.clipId
        # Get mediaclip thumbnail image
        self.clip = clip
        # We need thumbnail concepts
        try:
            self.thumbnailConcepts = self.getThumbnailConcepts()
            # Load the clip into our video processor
            self.video = Video(self.clip.getVideoFile())
            self.noEval = False
        except:
            print 'Unable to find thumbnail, no evaluation possible.'
            self.noEval = True

    
    # Evaluate frames
    # Evaluate an array of frames
    # Returns: corrosponding array of boolean values, corrosponding array of vectors from CaffeNet
    def eval(self, frames):
        result = np.zeros(frames.shape[0])
        if self.noEval:
            return result
    
        vectors = self.net.classify(frames)
        for idx, vector in enumerate(vectors):
            # Compare mediaclip thumbnail concepts with frame concepts
            
            # Cosine distance
            dist = 1 - spatial.distance.cosine(vector, self.thumbnailConcepts)
            
            result[idx] = dist
        
        return result, vectors
        
        
    # Evaluate a specific frame from the video
    # Returns True / False
    # Accepts framenumber
    def evalFrame(self, frameNumber):
        if self.noEval:
            warnings.warn('No evaluation possible, will always return false')
            return False
        
        # Get concepts for frame with caffenet
        frame = self.video.getFrame(frameNumber)
        
        return self.eval([frame])[0]
    
    
    
    # Get concepts for mediaclip thumbnail image with caffenet
    def getThumbnailConcepts(self):
        thumbnail = self.clip.getThumbnail()
        
        if thumbnail != False:
            frame = self.net.loadImage(thumbnail)
            return self.net.classify([frame])[0]
        else:
            raise Warning('No thumbnail found!')
    
    
    # Returns true when we can do evaluation, false when we can not
    def canEval(self):
        return not self.noEval