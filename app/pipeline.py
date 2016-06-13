import numpy as np
import matplotlib.pyplot as plt
import sys

sys.dont_write_bytecode = True

from sklearn import svm, grid_search, datasets

from classes.metadata import Metadata
from classes.data import DataProvider
from classes.clip import Clip
from classes.evaluation import Evaluation
from classes.candidates import Candidates

class Pipeline:
    
    def __init__(self):
        self.dataProvider = DataProvider()
        self.clips = self.dataProvider.getClips()
        
        self.frameInterval = 25
        self.fragmentLength = 5
        
        # kModifier: BOF for every kModifier * frameInterval, thus K + 1 for each kModifier seconds
        self.kModifier = 15.0
        # Percentage of candidates to set correct
        self.percentile = 25.0
        
        
    def getMetadata(self):
        self.metadata = Metadata(self.clips, False)
    
    def setFrameInterval(self, interval):
        self.frameInterval = interval
    
    def gatherData(self, numberOfClips):
        allVectors = []
        allClasses = []
        
        self.getMetadata()
        # Build data that we use to train SVM model
        for idx, val in enumerate(self.clips):
            
            logIndicator = '('+str(idx)+'/'+str(len(self.clips))+') '
            print logIndicator + 'Evaluating clip '+val['id']
            
            clip = Clip(val, "/Volumes/Jorick van Hees/video-data/files/")
            if not clip.hasVideo():
                print logIndicator+'Clip has no video.'
                continue
            
            clipEval = Evaluation(clip)
            if not clipEval.canEval():
                print logIndicator+'Unable to evaluate.'
                continue
            
            metadataVector = self.metadata.getVectorsByClip(clip)
            if len(metadataVector) is 0:
                print logIndicator+'No metadata available.'
                continue
            
            metadataVectorArray = self.metadata.vectorsToArray(metadataVector)
            
            candidatesGen = Candidates(clip, self.kModifier)
            
            # Returns candidate starting frame numbers
            candidateList = candidatesGen.get(self.fragmentLength)
        
            # Get average concept vector for every candidate fragment
            concepts = np.zeros( (len(candidateList),1000) )            
            for idx, candidateIndex in enumerate(candidateList):
                concepts[idx] = self.getFragmentConcepts(clip, candidateIndex)
            
            results = clipEval.eval(concepts)
            
            # Calculate percentile from number of candidates
            classes = self.thresholdResults(results, self.percentile)
            
            # Combine concept vectors and metadata vector
            # We need to concatenate the metadata vector to the vectors for ALL frames 
            for concept in concepts:
                allVectors.append(np.concatenate([concept, metadataVectorArray]))
                
            # Populate global data with items from this clip
            allClasses.extend(classes)
            
            if idx > numberOfClips:
                break
        
        vectorsArray = np.array(allVectors)
        classesArray = np.array(allClasses)
        return vectorsArray, classesArray
    
    
    def buildModel(self, numberOfClips=None):
        if numberOfClips == None:
            numberOfClips = len(self.clips)
        
        try:
            allVectors = np.load('tmp/allVectors.npy')
            allResults = np.load('tmp/allResults.npy')
        except (IOError):
            allVectors, allResults = self.gatherData(numberOfClips)
            np.save('tmp/allVectors.npy', allVectors)
            np.save('tmp/allResults.npy', allResults)
        
        
        # Start building model with allVectors and allResults
        # Do a grid search to the best C and gamma for both linear and rbf kernels
        
        print allResults
        
        SVM = svm.SVC(cache_size=1000)
        param_grid = [
            {'C': [1000, 10000, 100000], 'gamma': [1, 10, 100], 'kernel': ['rbf']}, # Gaussian kernel
        ]
        grid = grid_search.GridSearchCV(SVM, param_grid, n_jobs=-1, verbose=1, cv=10, refit=True)
        print 'Training SVM Model with '+str(len(allVectors))+' classified frames...'
        grid.fit(allVectors, allResults)
        
        print 'Best params: '+str(grid.best_params_)+' with score: '+str(grid.best_score_)
    
    
    def getFragmentConcepts(self, clip, start):
        end = start + self.fragmentLength
        concepts = clip.getConcepts(start, end)
        return np.mean(concepts, axis=0)
    
    
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