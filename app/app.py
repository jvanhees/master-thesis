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
import cv2

from classes.video import Video
from classes.caffenet import CaffeNet
from classes.metadata import Metadata
from classes.data import DataProvider, Clip
#from classes.evaluation import Evaluate

data = DataProvider()
clips = data.getClips()

#metadataModel = Metadata(clips, cache=False)

for index, clip in enumerate(clips):
    clip = Clip(clip)

    print clip.getThumbnail()

# clip = Clip(clips[1])
#
# print clip.getThumbnail()
    

# metadataVector = metadataModel.getVectorsByClip(clip.getClip())
#
# video = Video(clip.getVideoFile())
# # Video analysis
# frame = video.getFrame(25)
#
# net = CaffeNet()
#
# predictions = net.classify([frame])
#
# vectors = metadataModel.vectorsToArray(metadataVector)
#
# result = np.concatenate((vectors, predictions[0]))


# for index, prediction in enumerate(predictions):
#     top_ind = net.getTopConcepts(prediction)
#     labels = net.getLabeledConcepts(prediction, top_ind)
#
#
#     print(str(index) + ': ' + labels[0][1] + '(' + str(labels[0][0]) + ')')
#
#
# raw_input("Press Enter to exit...")