import numpy as np
import cv2

def BGRtoRGB(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)