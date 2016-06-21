import os.path
import json
from pprint import pprint
from gensim import corpora, models, similarities
from gensim import matutils
from collections import defaultdict
import numpy as np

class Metadata:
    
    # Todo:
    # Filter out common tags like "Irish Examiner"
    
    stoplist = set('for a of the and to in'.split())
    
    def __init__(self, data, modelType):
        if data != None:
            self.data = data
        else:
            raise NameError('No data provided!')
        
        self.modelType = modelType
        
        self.model = None
        
        self.__texts = []
        self.__dictionary = None
        self.__corpus = None
        self.__tfidf = None
        self.__tmpLocation = 'tmp/'
    
    
    def save(self):
        corpora.MmCorpus.serialize(self.__tmpLocation + 'corpus.mm', self.__corpus)
        self.__dictionary.save(self.__tmpLocation + 'dictionary.dict')
        self.model.save(self.__tmpLocation + 'model.lda')
    
    
    def load(self):
        if not os.path.isfile(self.__tmpLocation + 'dictionary.dict'):
            return False
        if not os.path.isfile(self.__tmpLocation + 'corpus.mm'):
            return False
        if not os.path.isfile(self.__tmpLocation + 'model.lda'):
            return False
        
        self.__dictionary = corpora.Dictionary.load(self.__tmpLocation + 'dictionary.dict')
        self.__corpus = corpora.MmCorpus(self.__tmpLocation + 'corpus.mm')
        LdaModel.load(self.__tmpLocation + 'model.lda', mmap='r')
        return True
        
    
    # Get metadatavectors from a clip
    # Accepts clipObject, returns LDA vector
    def getVectors(self, clip):
        if self.__dictionary == None:
            raise ValueError('Dictionary not available!')
        
        texts = self.prepareClip(clip)
        vec_bow = self.__dictionary.doc2bow(texts)
        
        vec = self.model[vec_bow] # convert the query to LSI space
        return matutils.sparse2full(vec, self.model.num_topics)
        
    
    def prepareString(self, document):
        # Remove words from stoplist, lowercase string and split in list of words (tokens)
        ret = [word for word in document.lower().split() if word not in self.stoplist]
        return ret
    
    
    # Returns text string with all relevant metadata fields
    def prepareClip(self, clip):
        string = clip.getMetadataBlob()
        # Return tokens
        return self.prepareString(string)
    
    
    def vectorsToArray(self, vectors):
        return np.array([x[1] for x in vectors])
    
    
    def createModel(self, clips, topics):
        self.__createDictionary(clips)
        self.__buildCorpus()
    
        # Train LDA (Latent Dirichlet Allocation)
        self.model = models.ldamodel.LdaModel(self.__corpus, id2word=self.__dictionary, num_topics=topics)
    
    
    # Create a dictionary with the provided clips
    def __createDictionary(self, clips):
        self.documents = []
        # Create list with all clip token lists
        for c in clips:
            self.documents.append(self.prepareClip(c))
        
        # Calculate frequency of words
        frequency = defaultdict(int)
        for text in self.documents:
            for token in text:
                frequency[token] += 1
        
        # Remove words (tokens) that occur only once
        self.__texts = [[token for token in text if frequency[token] > 1] for text in self.documents]
        
        # Build dictionary with these words
        self.__dictionary = corpora.Dictionary(self.__texts)
        
        self.__dictionary.save(self.__tmpLocation + 'dictionary.dict')
        return self.__dictionary
    
    
    def __buildCorpus(self):
        # Create a bag of words corpus for all texts
        self.__corpus = [self.__dictionary.doc2bow(text) for text in self.__texts]
        # Save for later use
        corpora.MmCorpus.serialize(self.__tmpLocation + 'corpus.mm', self.__corpus)
        
        return self.__corpus