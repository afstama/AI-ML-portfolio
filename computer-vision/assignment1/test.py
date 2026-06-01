import numpy as np
import cv2
from framee import *

cap = cv2.VideoCapture(0)
ctr = 0
prevMask = None

while True:
    _, frame = cap.read()
    ctr += 1

    #1 frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1, 10, 60, 0.9)
    #2 frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 10, 60, 0.9)
    #3 frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 10, 20, 0.5)
    #4 frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 70, 60, 0.9)
    #5 frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 70, 100, 0.9)
    #6 frame = hough(frame, cv2.HOUGH_GRADIENT, 1, 10, 70, 80)
    frame = hough(frame, cv2.HOUGH_GRADIENT, 1.5, 10, 100, 100)

    # if ctr < 100:
    #     frame, crop1 = makeTemplate(frame)
    # cv2.imshow('frame', frame)
    # if crop1 is not None:
    #     cv2.imshow('crop', crop1)
    #     cv2.imshow('match', matchTemplate(frame, crop1))

    # if prevMask is None:
    #     frame, prevMask = draw(frame)
    # else:
    #     frame, prevMask = draw(frame, prevMask)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()