import matplotlib.pyplot as plt
import numpy as np
from sklearn.externals import joblib

from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import normalize

from metadata import Metadata
from data import DataProvider

class Topics:
    
    def __init__(self):
        self.metadata = Metadata(True, 'lda')
        self.dataProvider = DataProvider()
        self.topicFile = 'tmp/topics.npy'
        self.kMeansFile = 'tmp/kmeans.pkl.npy'
    
    
    def gatherData(self, t):
        self.clips = self.dataProvider.getClips()        
        self.model = self.metadata.createModel(self.clips, t)
    
    
    def getTopic(self, clip):
        vector = self.metadata.getVectors(clip)
        result = self.kmeans.predict(vector.reshape(1, -1))
        return result
        # return np.argmax(vector)
    
    
    def createTopics(self, clips, t, k):
        self.gatherData(t)
        self.createClusters(clips, k)
        
        topics = []
        for idx, clip in enumerate(clips):
            topics.append(self.getTopic(clip))
        
        self.topics = np.hstack(topics)
        
        return self.topics
    
    
    def save(self):
        self.metadata.save()
        np.save(self.topicFile, self.topics)
        joblib.dump(self.kmeans, self.kMeansFile) 
    
    
    def load(self):
        if not self.metadata.load():
            return False
        
        try:
            self.topics = np.load(self.topicFile)
            self.kmeans = joblib.load(self.kMeansFile) 
            return True
        except (IOError):
            return False
    
    
    # ------------------------------------------------
    # K Means on topic data...
    
    def createClusters(self, clips, k):
        vectors = []
        for idx, clip in enumerate(clips):
            vectors.append(self.metadata.getVectors(clip))
        
        self.vectors = np.vstack(vectors)
        
        self.clusterKMeans(self.vectors, k)
        
    
    def clusterKMeans(self, data, k):
        self.kmeans = KMeans(
            n_clusters=k,
            init='k-means++',
            n_init=10,
            max_iter=300,
            tol=0.0001,
            precompute_distances='auto',
            verbose=1,
            random_state=None,
            copy_x=True,
            n_jobs=1)
            
        self.kmeans.fit(data);
        
        return self.kmeans.inertia_