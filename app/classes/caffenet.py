import os
import sys
import numpy as np
import caffe

class CaffeNet:
    
    def __init__(self):
        caffe_root = '/Users/JVH/Development/caffe/'
        # RGB mode
        self.channels = 3
        # Load model
        if os.path.isfile(caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'):
            print 'CaffeNet found.'
        else:
            print 'CaffeNet not found.'
            
        caffe_root = '/Users/JVH/Development/caffe/'

        # Load labels
        labels_file = caffe_root + 'data/ilsvrc12/synset_words.txt'
        if not os.path.exists(labels_file):
            print 'Labels not found.'

        self.labels = np.loadtxt(labels_file, str, delimiter='\t')

        model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
        model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

        caffe.set_device(0)  # if we have multiple GPUs, pick the first one
        caffe.set_mode_gpu()

        # Start net
        self.net = caffe.Classifier(model_def, model_weights,
                               mean=np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1),
                               channel_swap=(2,1,0),
                               raw_scale=255,
                               image_dims=(256, 256))
                               
                               
    def getLabels(self):
        return self.labels
    
    def loadImage(self, image):
        return caffe.io.load_image(image)
    
    def classify(self, frames):
        return self.net.predict(frames)
    
    def getTopConcepts(self, output, count=None):
        # Returns indexes of top concepts
        if count is None:
            count = 5
            
        return output.argsort()[::-1][:count]  # reverse sort and take five largest items
        
    def getLabeledConcepts(self, output_prob, top_inds):
        return zip(output_prob[top_inds], self.labels[top_inds])