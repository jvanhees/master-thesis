import numpy as np
import cv2
from caffenet import CaffeNet
from video import Video
from data import Clip


frames = 25

# Evaluate frames for a specific clip.
class Evaluate:
    
    def __init__(self, clip):
        print "Starting evaluation for clip " + clip['id']
        # Get mediaclip thumbnail image
        self.clip = Clip(clip)
        # Init caffenet for evaluation
        self.net = CaffeNet()
        # We need thumbnail concepts
        try:
            self.thumbnailConcepts = self.getThumbnailConcepts()
            # Load the clip into our video processor
            self.video = Video(self.clip.getVideoFile())
            self.noEval = False
        except:
            self.noEval = True
            raise Warning('No thumbnail was found, no evaluation possible')

    
    # Evaluate a specific frame from the video
    # Returns True / False
    # Accepts video, framenumber
    def evalFrame(self, frameNumber):
        if self.noEval:
            raise Warning('No evaluation possible, will always return false')
            return False
        
        # Get concepts for frame with caffenet
        frame = self.video.getFrame(frameNumber)
        
        frameConcepts = self.net.classify([frame])
        
        # Compare mediaclip thumbnail concepts with frame concepts
        dist = np.linalg.norm(frameConcepts[0] - self.thumbnailConcepts)
        
        if dist < 0.3:
            return True
        else:
            return False
        
        # Decide True / False
    
    
    # Get concepts for mediaclip thumbnail image with caffenet
    def getThumbnailConcepts(self):
        thumbnail = self.clip.getThumbnail()
        
        if thumbnail != False:
            frame = self.net.loadImage(thumbnail)
            return self.net.classify([frame])[0]
        else:
            return False