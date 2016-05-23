import numpy as np
import matplotlib.pyplot as plt

from classes.video import Video
from classes.caffenet import CaffeNet
from classes.metadata import Metadata
from classes.data import DataProvider, Clip
from classes.evaluation import Evaluate

class Pipeline:
    
    def __init__(self):
        self.dataProvider = DataProvider()
        self.clips = self.dataProvider.getClips()
        
        self.frameInterval = 25
        
        self.metadata = Metadata(self.clips, False)
    
    
    def setFrameInterval(self, interval):
        self.frameInterval = interval
    
    
    def buildModel(self, numberOfClips=None):
        if numberOfClips == None:
            numberOfClips = len(self.clips)
        
        # Prepare results list
        allResults = []
        allVectors = []
        # Build data that we use to train SVM model
        for idx, val in enumerate(self.clips):
            # Instantiate clip
            clip = Clip(val)
            # Instantiate evaluation
            evaluation = Evaluate(clip)
            # Evaluate every frame at once
            if evaluation.canEval():
                
                # Load video
                video = Video(clip.getVideoFile())
                # Get the frame for every second in video
                frames = video.getFrames(25)
                
                # Add the result to the results array
                results, vectors = evaluation.eval(frames)
                
                #plt.plot(results)
                #plt.title('Similarity between frames and thumbnail for video: ' + clip.getTitle())
                #plt.show()                
                
                # Get metadata vector for clip
                metadataVector = self.metadata.getVectorsByClip(clip)
                metadataVectorArray = self.metadata.vectorsToArray(metadataVector)

                # Combine concept vectors and metadata vector
                # We need to concatenate the metadata vector to the vectors for ALL frames
                            
                for vector in vectors:
                    allVectors.append(np.concatenate([vector, metadataVectorArray]))
                    
                # Populate global data with items from this clip
                allResults.extend(results)
    
            if idx > numberOfClips:
                break
            
        # Start building model with allVectors and allResults
        
        print vectors.shape