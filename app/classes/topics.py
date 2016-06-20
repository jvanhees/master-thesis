import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn.preprocessing import normalize

from metadata import Metadata
from data import DataProvider

class Topics:
    
    def __init__(self):
        self.metadata = Metadata(False, 'lda')
        self.dataProvider = DataProvider()
    
    
    def gatherData(self, t):
        clips = self.dataProvider.getClips()        
        model = self.metadata.createModel(clips, t)
    
    
    def getTopic(self, clip):
        vector = self.metadata.getVectors(clip)
        return np.argmax(vector)
    
    
    def createTopics(self, clips, k):
        self.gatherData(k)
        topics = []
        for idx, clip in enumerate(clips):
            topics.append(self.getTopic(clip))
        
        self.topics = np.hstack(topics)
        return self.topics
    
    
    # ------------------------------------------------
    # K Means on topic data...
    
    def createClusters(self, k):
        
        topicResults = []
        for t in [3, 5, 10, 20]:
            results = []
            vectors = self.gatherData(t)
            
            kArray = range(2, 30)
            for k in kArray:
                print '('+str(t)+') Clustering with K = '+str(k)
                results.append(self.clusterKMeans(vectors, k))
            
            topicResults.append(results)
            
        topicResults = np.vstack(topicResults)
        normalize(topicResults, norm='l1', axis=1, copy=False)
        
        for idx, topic in enumerate(topicResults):
            plt.plot(topic)
        
        plt.ylabel('Normalised K-Means inertia')
        plt.xlabel('# of K')
        plt.show()
    
    def clusterKMeans(self, data, k):
        self.kmeans = KMeans(
            n_clusters=k,
            init='k-means++',
            n_init=10,
            max_iter=300,
            tol=0.0001,
            precompute_distances='auto',
            verbose=0,
            random_state=None,
            copy_x=True,
            n_jobs=1)
            
        self.kmeans.fit(data);
        
        return self.kmeans.inertia_