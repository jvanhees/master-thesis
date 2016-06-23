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
import getopt

sys.dont_write_bytecode = True

from pipeline import Pipeline
from classes.data import DataProvider
from classes.videoWriter import VideoWriter

#metadataModel = Metadata(clips, cache=False)

pipeline = Pipeline()

if not pipeline.load():
    pipeline.createTopicModels(10)
    pipeline.save()

clips = pipeline.getClips()

for idx, clip in enumerate(clips):
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
