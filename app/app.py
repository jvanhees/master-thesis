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

#metadataModel = Metadata(clips, cache=False)

pipeline = Pipeline()

pipeline.createClusters(10)

# params = pipeline.getParams()

#params = {'kernel': 'rbf', 'C': 10000, 'gamma': 100}
#print params

#pipeline.loadSVM(params)

#print pipeline.predict(data.getClip('2521541'))