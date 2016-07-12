import math
import numpy as np
from scipy import spatial
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.externals import joblib

from clip import Clip

class Candidates:
    
    def __init__(self, clip, kModifier):
        self.clip = clip
        self.kmeansfile = 'tmp/clipkmeans/'+str(clip.getClipId())+'.pkl'
        self.concepts = self.clip.getConcepts()
        # k = length of clip in seconds / kModifier
        
        self.k = int(math.ceil(len(self.concepts) / kModifier))
        
        if not self.load():
            self.bofs = self.createBOF(self.k)
            self.save()
        
    
    def get(self, fragmentLength):
        # Create an array we can fill with distances, axis 1 = bofs, axis 2 = frames
        fragmentDistances = np.zeros((self.k, len(self.concepts)))

        for i, concept in enumerate(self.concepts):
            # Get concepts for frame + frames * n
            end = i + fragmentLength
            fragment = self.concepts[i:end]
            # Combine concepts with max
            fragmentConcept = np.amax(fragment, axis=0)

            for j, bof in enumerate(self.bofs):
                # Calculate cosine distance between video fragment representation and bof
                fragmentDistances[j,i] = 1 - spatial.distance.cosine(bof, fragmentConcept)

        # normalise over frame axis
        normFragmentDistances = normalize(fragmentDistances, norm='l1', axis=0)

        # select frame with lowest distance for each BOF
        candidateIndexes = np.argmax(normFragmentDistances, axis=1)
        
        return candidateIndexes
    
    def load(self):
        try:
            self.kmeans = joblib.load(self.kmeansfile)
            self.bofs = self.kmeans.cluster_centers_
            print 'Clip candidate Kmeans loaded.'
            return True
        except (IOError):
            print 'Clip candidate Kmeans NOT loaded.'
            return False
    
    
    def save(self):
        joblib.dump(self.kmeans, self.kmeansfile)
    
    
    # Create K Bag of Fragments
    def createBOF(self, k):
        # Create BOF with K-mean
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
            
        self.kmeans.fit(self.concepts);
        
        return self.kmeans.cluster_centers_
        