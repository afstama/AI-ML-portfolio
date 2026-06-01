import cv2
import numpy as np
import matplotlib.pyplot as plt

# smoothing: https://docs.opencv.org/4.x/d4/d13/tutorial_py_filtering.html
# color changing / disappearing: https://subscription.packtpub.com/book/data/9781789537147/1/ch01lvl1sec09/object-detection-using-color-in-hsv


img = cv2.imread('objects.png')
# cv2.imshow('image', img)
# cv2.waitKey(0)

def toGrayscale(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    return grayImage

def blurGaussian(image):
    blur = cv2.GaussianBlur(image, (5, 7), 5)
    # in (5, 7) - 5 is horizontal, and 7 is vertical blur
    # larger sigma -> larger blur (but comprehensive, like shaking)
    # bigger kernel size -> more blur
    return blur

def blurBilateral(image):
    # keeping edges sharp, slower tho
    blur = cv2.bilateralFilter(image, 9, 75, 75)
    # first paramter controls 'cartoonishness' of smoothing
    # second parameter controls blurring
    # third parameter not that important ??
    return blur

def grabHSV(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower_blue = np.array([110,50,50])
    # upper_blue = np.array([130,255,255])

    # lower_orange = np.array([5, 50, 50])
    # upper_orange = np.array([15, 255, 255])

    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255]) 

    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(image, image, mask= mask)

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.imshow('res', res)
    cv2.waitKey(0)
    return

def grabRGB(image):
    # lower_blue = np.array([100, 0, 0])
    # upper_blue = np.array([255, 100, 100])

    # lower_orange = np.array([150, 75, 0])
    # upper_orange = np.array([255, 150, 50])   ### not correct color range

    lower_green = np.array([0, 100, 0])      # Adjust these values as needed
    upper_green = np.array([100, 255, 100])

    mask = cv2.inRange(image, lower_green, upper_green)
    res = cv2.bitwise_and(image, image, mask= mask)

    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.imshow('mask', mask)
    cv2.waitKey(0)
    cv2.imshow('res', res)
    cv2.waitKey(0)
    return

grabHSV(img)
# grabRGB(img)
cv2.destroyAllWindows()