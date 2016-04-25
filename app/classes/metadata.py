import os.path
import json
from pprint import pprint
from gensim import corpora, models, similarities
from collections import defaultdict

class Metadata:
    
    # Todo:
    # Filter out common tags like "Irish Examiner"
    
    stoplist = set('for a of the and to in'.split())
    
    def __init__(self, metadataFile):
        
        self.file = metadataFile
        
        self.data = None
        
        self.__texts = []
        self.__dictionary = None
        self.__corpus = None
        self.__tmpLocation = 'tmp/'
        
        self.lsi = None
        
        self.__loadModel()
    
    def __loadData(self):
        with open(self.file) as data_file:
            self.data = json.load(data_file)
    
    
    def __buildCorpus(self):
        self.documents = []
        for clip in self.data['items']:
            if 'title' in clip:
                self.documents.append(clip['title'])
            if 'description' in clip:
                self.documents.append(clip['description'])
            if 'cat' in clip:
                self.documents.append(' '.join(clip['cat']))
                
        texts = [[word for word in document.lower().split() if word not in self.stoplist] for document in self.documents]
        
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
                
        self.__texts = [[token for token in text if frequency[token] > 1] for text in texts]
        
        self.__dictionary = corpora.Dictionary(texts)
        
        corpus = [self.__dictionary.doc2bow(text) for text in texts]
        corpora.MmCorpus.serialize(self.__tmpLocation + 'corpus.mm', corpus)
        
        return corpus
    
    
    def __loadCorpus(self):
        if self.data == None:
            self.__loadData()
            
        if os.path.isfile(self.__tmpLocation + 'corpus.mm'):
            self.__corpus = corpora.MmCorpus(self.__tmpLocation + 'corpus.mm')
        else:
            self.__corpus = self.__buildCorpus()
    
        
    def __createModel(self):
        tfidf = models.TfidfModel(self.__corpus) # step 1 -- initialize a model
        corpus_tfidf = tfidf[self.__corpus]
        
        lsi = models.LsiModel(corpus_tfidf, id2word=self.__dictionary, num_topics=200) # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
        
        lsi.save(self.__tmpLocation + 'model.lsi')
        return lsi
        
    
    def __loadModel(self):
        if os.path.isfile(self.__tmpLocation + 'model.lsi'):
            self.lsi = models.LsiModel.load(self.__tmpLocation + 'model.lsi')
        else:
            self.lsi = self.__createModel()