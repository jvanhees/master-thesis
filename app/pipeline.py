import numpy as np
import matplotlib.pyplot as plt
import sys

from sklearn import svm, grid_search, datasets

from classes.video import Video
from classes.caffenet import CaffeNet
from classes.metadata import Metadata
from classes.data import DataProvider
from classes.clip import Clip
from classes.concept_evaluation import ConceptEvaluation
from classes.event_evaluation import EventEvaluation

class Pipeline:
    
    def __init__(self):
        self.dataProvider = DataProvider()
        self.clips = self.dataProvider.getClips()
        
        self.frameInterval = 25
        
        self.metadata = Metadata(self.clips, False)
    
    
    def setFrameInterval(self, interval):
        self.frameInterval = interval
    
    
    def thresholdResults(self, values, thresholdPercentage):
        threshold = np.percentile(values, (100.0 - thresholdPercentage))
        results = []
        # Get top 10 percent, so get values that are bigger than the 100 - 10 = 90th percentile
        for idx, val in enumerate(values):
            if val > threshold:
                results.append(1)
            else:
                results.append(0)
        
        return results
    
    
    def buildModels(self):
        # Prepare results list
        allResults = []
        allVectors = []
        # Build data that we use to train SVM model
        for idx, val in enumerate(self.clips):
            clip = Clip(val, "/Volumes/Jorick van Hees/video-data/files/")
            if not clip.hasVideo():
                continue

            eventEval = EventEvaluation(clip)
            concepts = clip.getConcepts()
            if concepts is -1:
                continue
            mean = eventEval.eval(concepts)

            plt.plot(mean)

            conceptEval = ConceptEvaluation(clip)

            if conceptEval.canEval():
                concepts = clip.getConcepts()

                results = conceptEval.eval(concepts)
                plt.plot(results)

            plt.title('Similarity between frames and full video: ' + clip.getTitle())
            plt.show()
    
    def buildEventModel(self):
        
        for idx, val in enumerate(self.clips):
            
            clip = Clip(val, "/Volumes/Jorick van Hees/video-data/files/")
            concepts = clip.getConcepts()
            if concepts is -1:
                break

            eventEval = EventEvaluation(clip)
            mean = eventEval.eval(concepts)
        
            plt.plot(mean)
            plt.plot(max)
            plt.title('Similarity between frames and full video: ' + clip.getTitle())
            plt.show()
        
        
    def gatherConceptData(self, numberOfClips):
        # Prepare results list
        allResults = []
        allVectors = []
        # Build data that we use to train SVM model
        for idx, val in enumerate(self.clips):
            # Instantiate clip
            clip = Clip(val, '/Volumes/Jorick van Hees/video-data/files/')
            if not clip.hasVideo():
                continue
                
            # Instantiate evaluation
            conceptEval = ConceptEvaluation(clip)
            # Evaluate every frame at once
            if conceptEval.canEval():
                
                # Get metadata vector for clip
                metadataVector = self.metadata.getVectorsByClip(clip)
                if len(metadataVector) is 0:
                    continue
                
                metadataVectorArray = self.metadata.vectorsToArray(metadataVector)
                
                concepts = clip.getConcepts()
                # Add the result to the results array
                results = conceptEval.eval(concepts)
                
                classes = self.thresholdResults(results, 10.0)
                
                print results;
                plt.plot(results)
                plt.plot(classes)
                plt.title('Similarity between frames and thumbnail for video: ' + clip.getTitle())
                plt.show()             

                # Combine concept vectors and metadata vector
                # We need to concatenate the metadata vector to the vectors for ALL frames
                            
                for concept in concepts:
                    allVectors.append(np.concatenate([concept, metadataVectorArray]))
                    
                # Populate global data with items from this clip
                allResults.extend(results)
                
                
            if idx > numberOfClips:
                break
        
        allVectorsArray = np.array(allVectors)
        allResultsArray = np.array(allResults)
        return allVectorsArray, allResultsArray
    
    
    def buildConceptModel(self, numberOfClips=None):
        if numberOfClips == None:
            numberOfClips = len(self.clips)
        
        try:
            allVectors = np.load('tmp/allVectors.npy')
            allResults = np.load('tmp/allResults.npy')
        except (IOError):
            allVectors, allResults = self.gatherConceptData(numberOfClips)
            np.save('tmp/allVectors.npy', allVectors)
            np.save('tmp/allResults.npy', allResults)
        
        
        # Start building model with allVectors and allResults
        # Do a grid search to the best C and gamma for both linear and rbf kernels
        
        SVM = svm.SVC(cache_size=1000)
        param_grid = [
            {'C': [1000, 10000, 100000], 'gamma': [1, 10, 100], 'kernel': ['rbf']}, # Gaussian kernel
        ]
        grid = grid_search.GridSearchCV(SVM, param_grid, n_jobs=4, verbose=1, cv=10, refit=True)
        print 'Training SVM Model with '+str(len(allVectors))+' classified frames...'
        grid.fit(allVectors, allResults)
        
        print 'Best params: '+str(grid.best_params_)+' with score: '+str(grid.best_score_)
        
        