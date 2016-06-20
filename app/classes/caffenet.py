import os
import sys
import numpy as np
import caffe

class CaffeNet:
        
    def __init__(self):
        # RGB mode
        self.channels = 3
        
        # Load model
        self.caffe_root = '/Users/JVH/Development/caffe/'
        if not os.path.isfile(self.caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
            raise CaffeError('CaffeNet not found')

        # Load labels
        labels_file = self.caffe_root + 'data/ilsvrc12/synset_words.txt'
        if not os.path.exists(labels_file):
            print 'Labels not found.'

        self.labels = np.loadtxt(labels_file, str, delimiter='\t')
        
        self.loaded = False
    
    
    def load(self):
        print 'Initializing CaffeNet'
        model_def = self.caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
        model_weights = self.caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

        caffe.set_device(0)  # if we have multiple GPUs, pick the first one
        caffe.set_mode_gpu()

        # Start net
        self.net = caffe.Classifier(model_def, model_weights,
                               mean=np.load(self.caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                               channel_swap=(2,1,0),
                               raw_scale=255,
                               image_dims=(256, 256))
        self.loaded = True
    
                               
    def getLabels(self):
        return self.labels
    
    def loadImage(self, image):
        return caffe.io.load_image(image)
    
    def classify(self, frames):
        if not self.loaded:
            self.load()
        
        return self.net.predict(frames)
    
    def getTopConcepts(self, output, count=None):
        # Returns indexes of top concepts
        if count is None:
            count = 5
            
        return output.argsort()[::-1][:count]  # reverse sort and take five largest items
        
    def getLabeledConcepts(self, output_prob, top_inds):
        return zip(output_prob[top_inds], self.labels[top_inds])