import numpy as np
import json
from pprint import pprint

with open('data/data.json') as data_file:    
    data = json.load(data_file)

numberOfClips = 0
numberOfTags = 0

for clip in data['items']:
    numberOfClips = numberOfClips + 1
    if 'cat' in clip:
        numberOfTags = numberOfTags + len(clip['cat'])

print numberOfClips
print numberOfTags

print float(numberOfTags) / float(numberOfClips)