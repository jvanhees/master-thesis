#!/usr/bin/env python

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
sys.dont_write_bytecode = True

import numpy as np
import argparse
import matplotlib.pyplot as plt
from PIL import Image  

from pipeline import Pipeline
from classes.data import DataProvider
from classes.videoWriter import VideoWriter

from classes.helpers import BGRtoRGB

#metadataModel = Metadata(clips, cache=False)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start')
parser.add_argument('-e', '--end')
args = parser.parse_args()

pipeline = Pipeline()
data = DataProvider()

if not pipeline.load():
    print "Error, not loaded"
    sys.exit()
    pipeline.save()

# scores = []
# for k in range(15, 16):
#     print 'K = ' + str(k)
#     pipeline.createTopicModels(25, k)
#     score = pipeline.scores
#     scores.append(np.mean(score))
#
#     print 'Mean: ' + str(np.mean(score))


# fig = plt.figure()
# plt.bar(np.arange(len(scores)), scores, align='center', color='#D6B16D', linewidth=0.0)
#
# axes = plt.gca()
# axes.set_ylim([0.5,1])
# axes.set_xlim([-0.5,len(scores) - 0.5])
#
# fig.savefig('svm accuracy.png', dpi=300)

# T = 25
# K = 10

# scores = []
#
# scores.append(pipeline.createTopicModels(25, 10))
#
# plt.plot(scores)
# plt.show()



# clips = [2551267, 2653625, 2486497, 2465955, 2526352, 2553815, 2560692, 2547450, 2516436, 2487045]
clips = [2487045]


for idx, clipId in enumerate(clips):
    clip = data.getClip(clipId)
    
    if clip == False:
        continue
    
    vectors, candidateList = pipeline.getClipCandidateVectors(clip)
    frames = clip.getRawFrames()
    
    print candidateList

    videoWriter = VideoWriter(clip, 'output/')
    for idx, candidate in enumerate(candidateList):
        filename = clip.getClipId() + '('+ str(idx) +')'
        videoWriter.createVideo(candidate, candidate+5, filename)
    
    # print clip.getClipId(), 'Getting prediction'
#
#     result, scores = pipeline.predict(clip)
#
#     print clip.getClipId(), 'Writing video thumbnail ('+ str(result[0]) +')'
#     videoWriter = VideoWriter(clip, 'output/')
#     filename = clip.getClipId() + '('+ str(scores[0]) +')'
#     videoWriter.createVideo(result[0], result[0]+5, filename)
    
    

# np.argwhere(x>1)
# Pipeline is as follows:
# Build models:
    #
    # Get candidates for all clips in topic
    # Evaluate candidates for clips in topic
    #
    # Get candidates + results for each topic
    # Build model with all candidates for each topics
    
# Predict frames:
    # Get candidates for clip
    # Decide on topic
    # Insert candidate data in relevant model
    # Order prediction
