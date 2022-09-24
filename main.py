#!/usr/bin/env python3

import time

import cv2
import numpy as np
import pyfakewebcam
import threading
WIDTH = 480
HEIGHT = 480
DEVICE = '/dev/video2'

fake_cam = pyfakewebcam.FakeWebcam(DEVICE, WIDTH, HEIGHT)

window_name = 'virtual-camera'
cv2.namedWindow(window_name, cv2.WINDOW_GUI_EXPANDED)
cam = cv2.VideoCapture(0)
img1 = np.random.uniform(0, 255, (HEIGHT, WIDTH, 3)).astype('uint8')
img2 = np.random.uniform(0, 255, (HEIGHT, WIDTH, 3)).astype('uint8')

IMAGE = np.random.uniform(0, 255, (HEIGHT, WIDTH, 3)).astype('uint8')
FPS = 0.
FRAMES = 0

def readcam():
    global IMAGE, FPS, FRAMES
    old = time.time()
    while True:
        start = time.time()
        nxt_frame = int(start * 25 + 1) /25
        time.sleep( nxt_frame - start)

        r, IMAGE = cam.read()
        FRAMES += 1
        new = time.time()
        FPS = 1/(new - nxt_frame)
        old = new
        
CAMLOOP = threading.Thread(target=readcam)
CAMLOOP.start()

def printfps():
    global IMAGE, FPS, FRAMES
    while True:
        time.sleep(1)
        print("%.2f FPS (%d frames)" % (FPS, FRAMES))
        FRAMES = 0
threading.Thread(target=printfps).start()
        
while True:
    time.sleep(0.04)
    img2[0:480,0:480,:] = IMAGE[0:480,0:480,:]
    fake_cam.schedule_frame(img2)

cv2.destroyAllWindows()
