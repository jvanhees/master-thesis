import numpy as np
import matplotlib.pyplot as plt
import pylab
import timeit

import helpers.caffenet as caffenet

import helpers.video as video

#labels = caffenet.getLabels()
#result = caffenet.classify('data/cat-wallpaper-38.jpg');

# sort top five predictions from softmax output
#top_inds = result.argsort()[::-1][:5]  # reverse sort and take five largest items
#print 'probabilities and labels:'
#print zip(result[top_inds], labels[top_inds])

# print 'output label:', labels[output_prob.argmax()]

# Timer
# print timeit.timeit(net.forward, number=1)

video.loadVideo('data/vid.mp4')
video.getFrames(25)
video.closeVideo()