import numpy as np
import sys

sys.dont_write_bytecode = True

from sklearn import svm, grid_search, datasets
from sklearn.externals import joblib

from classes.topics import Topics
from classes.data import DataProvider
from classes.evaluation import Evaluation
from classes.candidates import Candidates
from classes.topics import Topics

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
        
        self.svmFile = 'tmp/svm.pkl'
        
        
    
    def setFrameInterval(self, interval):
        self.frameInterval = interval
    
    def gatherData(self):
        allVectors = []
        allClasses = []
        
        # Build data that we use to train SVM model
        for idx, clip in enumerate(self.clips):
            
            logIndicator = '('+str(idx)+'/'+str(len(self.clips))+') '
            print logIndicator + 'Evaluating clip '+clip.getClipId()
            
            if not clip.hasVideo():
                print logIndicator+'Clip has no video.'
                continue
            
            clipEval = Evaluation(clip)
            if not clipEval.canEval():
                print logIndicator+'Unable to evaluate.'
                continue
            
            vectors = self.getClipVectors(clip)
            
            results = clipEval.eval(vectors)
            
            # Calculate percentile from number of candidates
            classes = self.thresholdResults(results, self.percentile)
            
            for vector in vectors:
                allVectors.append(vector)
                
            # Populate global data with items from this clip
            allClasses.extend(classes)
        
        vectorsArray = np.array(allVectors)
        classesArray = np.array(allClasses)
        return vectorsArray, classesArray
    
    
    def getClipVector(self, clip):
        candidatesGen = Candidates(clip, self.kModifier)
        
        # Returns candidate starting frame numbers
        candidateList = candidatesGen.get(self.fragmentLength)
        
        # Get average concept vector for every candidate fragment
        concepts = np.zeros( (len(candidateList),1000) )
        for idx, candidateIndex in enumerate(candidateList):
            concepts[idx] = self.getFragmentConcepts(clip, candidateIndex)
            
                
        return concepts, candidateList
        
    
    def getData(self):
        try:
            allVectors = np.load('tmp/allVectors.npy')
            allResults = np.load('tmp/allResults.npy')
        except (IOError):
            allVectors, allResults = self.gatherData()
            np.save('tmp/allVectors.npy', allVectors)
            np.save('tmp/allResults.npy', allResults)
        
        return allVectors, allResults
    
    
    def getParams(self):
        allVectors, allResults = self.getData()        
        
        # Start building model with allVectors and allResults
        # Do a grid search to the best C and gamma for both linear and rbf kernels
        SVM = svm.SVC(cache_size=1000)
        param_grid = [
            {'C': [100, 1000, 10000, 100000], 'gamma': [10, 100, 1000], 'kernel': ['rbf']}, # Gaussian kernel
        ]
        grid = grid_search.GridSearchCV(SVM, param_grid, n_jobs=-1, verbose=1, cv=10, refit=True)
        print 'Training SVM Model with '+str(len(allVectors))+' classified frames...'
        grid.fit(allVectors, allResults)
        
        print 'Best params: '+str(grid.best_params_)+' with score: '+str(grid.best_score_)
        
        return grid.best_params_
    
    
    def createClusters(self, k):
        self.topics = Topics()
        
        self.topics.createClusters(k)
    
    
    def buildSVM(self, params):
        allVectors, allResults = self.getData()
        
        params['probability'] = True
        params['verbose'] = True
        
        self.SVM = svm.SVC()
        self.SVM.set_params(**params)
        self.SVM.fit(allVectors, allResults)
    
    
    def loadSVM(self, params):
        try:
            self.SVM = joblib.load(self.svmFile)
            print 'Loading SVM'
        except (IOError):
            print 'Building SVM'
            self.buildSVM(params)
            save = joblib.dump(self.SVM, self.svmFile, compress=9)
    
    
    def predict(self, clip):
        if not clip.hasVideo():
            raise NameError(logIndicator+'Clip has no video.')
        
        allVectors = []        
        vectors, candidateList = self.gatherClipData(clip)
        for vector in vectors:
            allVectors.append(vector)
        
        vectorArray = np.array(allVectors)
        
        #for candidate in candidateList:
            #clip.videoReader.showFrame(candidate * self.frameInterval)
            #raw_input("Press Enter to continue...")
        
        return self.SVM.decision_function(vectorArray)
    
    
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