from __future__ import print_function
import numpy as np
import argparse
import cv2
import os

# parse command line to add video arg
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

if not args.get("video", False):
	cap = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	cap = cv2.VideoCapture(args["video"])

dirname = 'analyze'
if not os.path.exists(dirname):
    os.mkdir(dirname)
    
print(cv2.__version__)
# cap = cv2.VideoCapture(videoname)
success,image = cap.read()
count = 0
success = True
diffs = []

fc = cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = cap.get(cv2.CAP_PROP_FPS)
print('Frame count: %d' % fc)
print('FPS: %d' % fps)

while success:
    success,image = cap.read()
    if count > 0 and count < (fc-10):
        diff = sum(sum(sum(abs(image-previmage))))
        diffs.append(diff)
        if diff > (370 * 1.8):
            cv2.imwrite(os.path.join(dirname, "frame%06d.jpg" % count), image)     # save frame as JPEG file
    previmage = image
    #print image.shape
    #print 'Read a new frame: ', success
    count += 1

diffa = np.asarray(diffs)
print(np.min(diffa))
print(np.max(diffa))
print(np.mean(diffa))
print(np.median(diffa))
print('Total frames: %d' % count)
