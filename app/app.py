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
import getopt

from classes.video import Video
from classes.caffenet import CaffeNet
from classes.metadata import Metadata
from classes.data import DataProvider, Clip
from classes.evaluation import Evaluate
from pipeline import Pipeline

#metadataModel = Metadata(clips, cache=False)

pipeline = Pipeline()

pipeline.buildModel()