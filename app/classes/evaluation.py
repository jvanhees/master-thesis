import numpy as np
import cv2
import warnings
from scipy import spatial

from caffenet import CaffeNet
from clip import Clip


frames = 25

# Evaluate frames for a specific clip.
class Evaluation:
    
    def __init__(self, clip):
        # Get mediaclip thumbnail image
        self.clip = clip
        # We need thumbnail concepts
        self.thumbnailConcepts = self.clip.getThumbnailConcepts()
        
        if self.thumbnailConcepts is False:
            self.noEval = True
        else:
            self.noEval = False

    
    # Evaluate frames
    # Evaluate an array of frames
    # Returns: corrosponding array of values, corrosponding array of vectors from CaffeNet
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
    
    
    # Returns true when we can do evaluation, false when we can not
    def canEval(self):
        return not self.noEval
    