import os
import sys
import numpy as np
import caffe

caffe_root = '/Users/JVH/Development/caffe/'

channels = 3

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

labels = np.loadtxt(labels_file, str, delimiter='\t')

model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'

caffe.set_device(0)  # if we have multiple GPUs, pick the first one
caffe.set_mode_gpu()

# Start net
net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(50,        # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # image size is 227x227

def getLabels():
    return labels

def classify(image):
    image = caffe.io.load_image(image)
    transformed_image = transformer.preprocess('data', image)
    
    net.blobs['data'].data[...] = transformed_image
    ### perform classification
    output = net.forward()
    
    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
    
    return output_prob

def setImageSize(x, y):
    net.blobs['data'].reshape(net.blobs['data'].shape[0], # batch size, dont change when setting img size
                              channels,
                              x, y)                       # Default size is 227x227

def setImageCount(count):
    net.blobs['data'].reshape(count, # batch size
                              channels,
                              net.blobs['data'].shape[2], net.blobs['data'].shape[3])  # Keep old image size
