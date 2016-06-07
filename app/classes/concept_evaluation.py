import numpy as np
import cv2
import warnings
from scipy import spatial

from caffenet import CaffeNet
from video import Video
from clip import Clip


frames = 25

# Evaluate frames for a specific clip.
class ConceptEvaluation:
    
    def __init__(self, clip):
        print "Starting evaluation for clip " + clip.clipId
        # Get mediaclip thumbnail image
        self.clip = clip
        # We need thumbnail concepts
        self.thumbnailConcepts = self.clip.getThumbnailConcepts()
        
        if self.thumbnailConcepts is False:
            print 'Unable to find thumbnail, no evaluation possible.'
            self.noEval = True
        else:
            self.noEval = False

    
    # Evaluate frames
    # Evaluate an array of frames
    # Returns: corrosponding array of boolean values, corrosponding array of vectors from CaffeNet
    def eval(self, vectors):
        results = []
        if self.noEval:
            return results
    
        for idx, vector in enumerate(vectors):
            # Compare mediaclip thumbnail concepts with frame concepts
            
            # Cosine distance
            dist = 1 - spatial.distance.cosine(vector, self.thumbnailConcepts)    
            
            results.append(dist)
        
        return results
        
        
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
    
    
    # Returns true when we can do evaluation, false when we can not
    def canEval(self):
        return not self.noEval
    