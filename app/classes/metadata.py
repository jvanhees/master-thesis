import os.path
import json
from pprint import pprint
from gensim import corpora, models, similarities
from collections import defaultdict
import numpy as np

from data import DataProvider
from clip import Clip

class Metadata:
    
    # Todo:
    # Filter out common tags like "Irish Examiner"
    
    stoplist = set('for a of the and to in'.split())
    
    def __init__(self, data, cache=None):
        
        if cache == None:
            self.cache = True
        else:
            self.cache = cache
        
        if data != None:
            self.data = data
        else:
            raise NameError('No data provided!')
        
        self.lsi = None
        
        self.__texts = []
        self.__dictionary = None
        self.__corpus = None
        self.__tmpLocation = 'tmp/'
        
        self.__loadDictionary()
        self.__loadCorpus()
        self.__loadModel()
    
    
    def getVectorsByClip(self, clip):
        texts = self.prepareClip(clip)
        vec_bow = self.__dictionary.doc2bow(texts)
        vec_lsi = self.lsi[vec_bow] # convert the query to LSI space
        return vec_lsi
    
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
    
    def __buildCorpus(self):
        if self.__dictionary == None:
            self.__loadDictionary()
        
        # Create a bag of words corpus for all texts
        corpus = [self.__dictionary.doc2bow(text) for text in self.__texts]
        # Save for later use
        corpora.MmCorpus.serialize(self.__tmpLocation + 'corpus.mm', corpus)
        
        return corpus
    
    
    def __loadCorpus(self):
        # Load from file, or generate with data
        if os.path.isfile(self.__tmpLocation + 'corpus.mm') and self.cache == True:
            self.__corpus = corpora.MmCorpus(self.__tmpLocation + 'corpus.mm')
        else:
            self.__corpus = self.__buildCorpus()
    
        
    def __createModel(self):
        # check if we have a corpus
        if self.__corpus == None:
            self.__loadCorpus()
        
        # Create tfidf (term frequency inverse document frequency)
        tfidf = models.TfidfModel(self.__corpus)
        corpus_tfidf = tfidf[self.__corpus]
        
        # Train LSI (Latent semantic indexing) transformation
        lsi = models.LsiModel(corpus_tfidf, id2word=self.__dictionary, num_topics=200) # initialize an LSI transformation
        #corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
        # Save for later use
        lsi.save(self.__tmpLocation + 'model.lsi')
        
        return lsi
    
    
    def __loadModel(self):
         # Load from file, or generate with data
        if os.path.isfile(self.__tmpLocation + 'model.lsi') and self.cache == True:
            self.lsi = models.LsiModel.load(self.__tmpLocation + 'model.lsi')
        else:
            self.lsi = self.__createModel()
    
    
    def __createDictionary(self):
        self.documents = []
        # Create list with all clip token lists
        for c in self.data:
            clip = Clip(c)
            self.documents.append(self.prepareClip(clip))
        
        # Calculate frequency of words
        frequency = defaultdict(int)
        for text in self.documents:
            for token in text:
                frequency[token] += 1
        
        # Remove words (tokens) that occur only once
        self.__texts = [[token for token in text if frequency[token] > 1] for text in self.documents]
        
        # Build dictionary with these words
        dictionary = corpora.Dictionary(self.__texts)
        
        dictionary.save(self.__tmpLocation + 'dictionary.dict')
        return dictionary
    
    
    def __loadDictionary(self):
         # Load from file, or generate with data
        if os.path.isfile(self.__tmpLocation + 'dictionary.dict') and self.cache == True:
            print 'Loading dictionary...'
            self.__dictionary = corpora.Dictionary()
            self.__dictionary.load(self.__tmpLocation + 'dictionary.dict')
        else:
            print 'Creating dictionary...'
            self.__dictionary = self.__createDictionary()