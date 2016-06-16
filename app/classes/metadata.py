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
    
    def __init__(self, data, modelType, cache=None):
        
        if cache == None:
            self.cache = True
        else:
            self.cache = cache
        
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
    
    
    # Get metadatavectors from a clip
    # Accepts clipObject, returns LDA vector
    def getVectors(self, clip):
        if self.__dictionary == None:
            raise ValueError('Dictionary not available!')
        
        texts = self.prepareClip(clip)
        vec_bow = self.__dictionary.doc2bow(texts)
        
        if self.modelType == 'lsi':
            vec_tfidf = self.__tfidf[vec_bow]
            vec = self.model[vec_tfidf] # convert the query to LSI space
            return matutils.sparse2full(vec, self.model.num_topics)
        
        if self.modelType == 'lda':
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
    
    
    # Create a dictionary with the provided clips
    def __createDictionary(self, clips):
        if os.path.isfile(self.__tmpLocation + 'dictionary.dict') and self.cache == True:
            print 'Loading dictionary...'
            self.__dictionary = corpora.Dictionary.load(self.__tmpLocation + 'dictionary.dict')
            return self.__dictionary
        else:
            print 'Creating dictionary...'
        
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
        if os.path.isfile(self.__tmpLocation + 'corpus.mm') and self.cache == True:
            self.__corpus = corpora.MmCorpus(self.__tmpLocation + 'corpus.mm')
            return self.__corpus
        
        # Create a bag of words corpus for all texts
        self.__corpus = [self.__dictionary.doc2bow(text) for text in self.__texts]
        # Save for later use
        corpora.MmCorpus.serialize(self.__tmpLocation + 'corpus.mm', self.__corpus)
        
        return self.__corpus
    
    
    def createModel(self, clips, topics):
        self.__createDictionary(clips)
        self.__buildCorpus()
        
        if self.modelType == 'lsi':
            self.__tfidf = models.TfidfModel(self.__corpus)
            self.__corpus_tfidf = self.__tfidf[self.__corpus]
            # Train LSI (Latent Semantic Indexing)
            self.model = models.LsiModel(self.__corpus_tfidf, id2word=self.__dictionary, num_topics=topics)
        
        if self.modelType == 'lda':
            # Train LDA (Latent Dirichlet Allocation)
            self.model = models.ldamodel.LdaModel(self.__corpus, id2word=self.__dictionary, num_topics=topics)