import numpy as np
import cv2
import warnings
from scipy import spatial

from caffenet import CaffeNet
from video import Video
from clip import Clip


frames = 25

# We try to extract abnormal events from the video which might be interesting for
# the video thumbnail. It works in the following way:
#
# Get concepts for every frame in the video (1FPS)
# Compute concepts for the whole video by using mean, mode or max
# Compare concepts for a single frame to the concepts for the whole video
# 
class EventEvaluation:
    
    # Init caffenet for evaluation
    net = CaffeNet()
    
    def __init__(self, clip):
        self.clip = clip

    
    # Evaluate frames
    # Evaluate an array of frames
    # Returns: corrosponding array of boolean values, corrosponding array of vectors from CaffeNet
    def eval(self, vectors):
        mean = self.getMean(vectors)
        
        result = np.zeros(vectors.shape[0])
    
        for idx, vector in enumerate(vectors):
            # Compare mediaclip thumbnail concepts with frame concepts
            
            # Cosine distance
            dist = 1 - spatial.distance.cosine(vector, mean)
            
            result[idx] = dist
        
        return result
    
    
    def getMean(self, vectors):
        # Calculate mean of vectors
        mean = np.mean(vectors, axis=0)
        return mean