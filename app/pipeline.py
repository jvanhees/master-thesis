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
        self.percentile = 50.0
        
        self.svmFile = 'tmp/svm.pkl.npy'
        
        self.params = {'kernel': 'rbf', 'C': 10, 'gamma': 100}
        
        self.scores = []
    
    
    def getClips(self):
        return self.clips
    
    def load(self):
        self.topics = Topics()
        if not self.topics.load():
            print 'Topics not loaded.'
            return False
        try:
            self.topicSVMs = np.load(self.svmFile)
            return True
        except (IOError):
            print 'SVM not loaded.'
            return False
    
    
    def save(self):
        self.topics.save()
        np.save(self.svmFile, self.topicSVMs)
    
    # Create models
    def createTopicModels(self, t, k):
        # Get topics for all clips
        self.topics = Topics()
        clipTopicList = self.topics.createTopics(self.clips, t, k)
        
        self.topicSVMs = []
        for topicIdx in range(k):
            indices = np.where(clipTopicList == topicIdx)
            topicClips = np.array(self.clips)[indices]
            
            vectors = []
            classes = []
            
            for idx, clip in enumerate(topicClips):
                clipEval = Evaluation(clip)
                if not clipEval.canEval():
                    continue
                
                clipVectors, candidates = self.getClipCandidateVectors(clip)
                results = clipEval.eval(clipVectors)
                
                classes.extend(self.thresholdResults(results, self.percentile))
                vectors.append(clipVectors)

            vectors = np.vstack(vectors)
            classes = np.array(classes)
            
            self.topicSVMs.append(self.initSVM(self.params, vectors, classes))
        
        return self.scores
        
    
    
    def initSVM(self, params, vectors, classes):
        params['probability'] = True
        params['verbose'] = False
        
        SVM = svm.SVC()
        SVM.set_params(**params)
        SVM.fit(vectors, classes)
        
        score = SVM.score(vectors, classes)
        
        self.scores.append(np.mean(score))
        
        return SVM


    
    def predict(self, clip):
        if not clip.hasVideo():
            raise NameError('Clip has no video.')
        
        # Get candidates for clip
        # Decide on topic
        # Insert candidate data in relevant model
        # Order prediction
        vectors, candidateList = self.getClipCandidateVectors(clip)
        topicIdx = self.topics.getTopic(clip)
        
        result = self.topicSVMs[topicIdx].predict_proba(vectors)
        
        return self.probabilityToRanking(result, candidateList)
        
    
    def probabilityToRanking(self, scores, candidates):
        sorted = np.sort(scores[:,1], axis=0)
        indices = np.argsort(scores[:,1], axis=0)
        result = candidates[indices]
        return result[::-1], sorted[::-1]
        
    
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
    
    
    def getParams(self, vectors, labels):   
        
        # Start building model with allVectors and allResults
        # Do a grid search to the best C and gamma for both linear and rbf kernels
        SVM = svm.SVC(cache_size=1000)
        param_grid = [
            {'C': [0.1, 1, 10], 'gamma': [10, 100, 1000], 'kernel': ['rbf']}, # Gaussian kernel
        ]
        grid = grid_search.GridSearchCV(SVM, param_grid, n_jobs=-1, verbose=1, cv=10, refit=True)
        print 'Training SVM Model with '+str(len(vectors))+' classified frames...'
        grid.fit(vectors, labels)
        print 'Best params: '+str(grid.best_params_)+' with score: '+str(grid.best_score_)
        return grid.best_params_, grid.best_score
    
    
    def setFrameInterval(self, interval):
        self.frameInterval = interval
    
    def getClipCandidateVectors(self, clip):
        candidatesGen = Candidates(clip, self.kModifier)
        
        # Returns candidate starting frame numbers
        candidateList = candidatesGen.get(self.fragmentLength)
        
        # Get average concept vector for every candidate fragment
        concepts = np.zeros( (len(candidateList),1000) )
        for idx, candidateIndex in enumerate(candidateList):
            concepts[idx] = self.getFragmentConcepts(clip, candidateIndex)
            
                
        return concepts, candidateList