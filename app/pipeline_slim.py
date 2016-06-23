import numpy as np
import sys

sys.dont_write_bytecode = True

from sklearn import svm, grid_search, datasets
from sklearn.externals import joblib

class Pipeline:
    
    def __init__(self):
        
        self.frameInterval = 25
        self.fragmentLength = 5
        
        # kModifier: BOF for every kModifier * frameInterval, thus K + 1 for each kModifier seconds
        self.kModifier = 15.0
        # Percentage of candidates to set correct
        self.percentile = 25.0
        
        self.svmFile = 'tmp/svm.pkl'
        
        
    def setFrameInterval(self, interval):
        self.frameInterval = interval
        
    
    def getData(self):
        allVectors = np.load('tmp/allVectors.npy')
        allResults = np.load('tmp/allResults.npy')
        
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