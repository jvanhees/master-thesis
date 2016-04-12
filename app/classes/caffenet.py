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
        self.net = caffe.Net(model_def,      # defines the structure of the model
                         model_weights,  # contains the trained weights
                         caffe.TEST)     # use test mode (e.g., don't perform dropout)

        # load the mean ImageNet image (as distributed with Caffe) for subtraction
        self.mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
        self.mu = self.mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values

        # create transformer for the input called 'data'
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})

        self.transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
        self.transformer.set_mean('data', self.mu)            # subtract the dataset-mean value in each channel
        self.transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
        self.transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

        # set the size of the input (we can skip this if we're happy
        #  with the default; we can also change it later, e.g., for different batch sizes)
        self.net.blobs['data'].reshape(1,        # batch size, default 1
                                       3,         # 3-channel (BGR) images
                                       227, 227)  # image size is 227x227

    def getLabels(self):
        return self.labels
    
    def loadImage(self, image):
        return caffe.io.load_image(image)
    
    def classify(self, frame):
        transformed_image = self.transformer.preprocess('data', frame)
        
        self.net.blobs['data'].data[...] = transformed_image
        ### perform classification
        output = self.net.forward()
    
        output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
        
        return output_prob
    
    def getTopConcepts(self, output_prob, count=None):
        # Returns indexes of top concepts
        if count is None:
            count = 5
            
        return output_prob.argsort()[::-1][:count]  # reverse sort and take five largest items
        
    def getLabeledConcepts(self, output_prob, top_inds):
        return zip(output_prob[top_inds], self.labels[top_inds])
    
    def setImageSize(self, x, y):
        self.net.blobs['data'].reshape(self.net.blobs['data'].shape[0], # batch size, dont change when setting img size
                                       self.channels,
                                       int(x), int(y))                       # Default size is 227x227

    def setImageCount(self, count):
        self.net.blobs['data'].reshape(int(count), # batch size
                                       self.channels,
                                       self.net.blobs['data'].shape[2], self.net.blobs['data'].shape[3])  # Keep old image size
