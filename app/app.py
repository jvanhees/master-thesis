# Suppress GLOG output for python bindings
# unless explicitly requested in environment
import os
if 'GLOG_minloglevel' not in os.environ:
    # Hide INFO and WARNING, show ERROR and FATAL
    os.environ['GLOG_minloglevel'] = '2'
    _unset_glog_level = True
else:
    _unset_glog_level = False

import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab
import timeit

from classes.video import Video
from classes.caffenet import CaffeNet

video = Video('../data/video/2441814.mp4')
frame = video.getFrame(5)

if frame is False:
    sys.exit("Unable to read frame")

video.closeVideo()

video.showFrame(frame)

net = CaffeNet()
vectors = net.classify(frame)
top_ind = net.getTopConcepts(vectors)

print(net.getLabeledConcepts(vectors, top_ind))

raw_input("Press Enter to exit...")