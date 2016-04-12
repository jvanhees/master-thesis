import numpy as np
import cv2

def loadVideo(videoFile):
    cap = cv2.VideoCapture(videoFile)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

def getFrames(interval):
    i = 0 # Frame 0
    # Prepare data, assume RGB channels
    data = np.zeroes((frames, width, height, 3), np.uint8)
    data = []
    
    success = True
    while cap.isOpened() & success:
        success, frame = cap.read()
        if i % interval == 0:
            print('found frame')

def closeVideo():
    # Release everything if job is finished
    cap.release()