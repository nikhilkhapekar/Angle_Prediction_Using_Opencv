import cv2
import imutils
import glob
import os
import numpy as np

# for demo purposes, we'll use some static JPGs
# of a green tape line
cwd = os.path.dirname(os.path.realpath(__file__))
full_path = os.path.join(cwd, 'images')

for filename in glob.glob(os.path.join(full_path, '*.jpg')):
    image = cv2.imread(filename)
    # https://github.com/jrosebr1/imutils has a handy resize func
    resized = imutils.resize(image, width=480)
    # convert to grayscale
    img = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    # threshold fairly agressively assuming a bold tape
    # color on a white background
    _, thresh = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY_INV)
    # get the countours
    cnts, _ = cv2.findContours(thresh, 
                                   cv2.RETR_TREE, 
                                   cv2.CHAIN_APPROX_SIMPLE)
    # sort the contours
    cnt = sorted(cnts, key=cv2.contourArea, reverse = True)
    # get the min rotated bounding rect of the largest one
    rect = cv2.minAreaRect(cnt[-1])
    # grab the height, width, and angle of that rect
    height, width = rect[1]
    angle = rect[2]
    # The value of OpenCV's angle depends on the rect's
    # height/width ratio. https://stackoverflow.com/a/24085639/292947
    if width < height:
        angle += 90
    # do something here with the angle to steer the car
    # we'll just print it
    print(angle)
    # and then, for visual purposes of this article, draw
    # the bounding box on and show the resized image
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(resized, [box], 0, (0, 0, 255), 2)
    cv2.imshow("Image", resized)
    cv2.waitKey(0)