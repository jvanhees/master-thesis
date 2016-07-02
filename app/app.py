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
import numpy as np
import argparse

sys.dont_write_bytecode = True

from pipeline import Pipeline
from classes.data import DataProvider
from classes.videoWriter import VideoWriter

#metadataModel = Metadata(clips, cache=False)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--start')
parser.add_argument('-e', '--end')
args = parser.parse_args()

pipeline = Pipeline()
data = DataProvider()

if not pipeline.load():
    pipeline.createTopicModels(25, 10)
    pipeline.save()

clips = pipeline.getClips()

if args.start == None:
    start = 0
else:
    start = int(args.start)

if args.end == None:
    end = len(clips) - 1
else:
    end = args.end

print start, end

clips = [2551267, 2653625, 2486497, 2465955, 2526352, 2553815, 2560692, 2547450, 2516436]


for idx, clipId in enumerate(clips):
    clip = data.getClip(clipId)
    
    if clip == False:
        continue

    print clip.getClipId(), 'Getting prediction'
    
    result, scores = pipeline.predict(clip)
    
    print clip.getClipId(), 'Writing video thumbnail ('+ str(result[0]) +')'
    videoWriter = VideoWriter(clip, 'output/')
    filename = clip.getClipId() + '('+ str(scores[0]) +')'
    videoWriter.createVideo(result[0], result[0]+5, filename)
    
    

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
