import numpy as np
import cv2
import textwrap

# 1.1
def grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# 1.2
def blurGaussian(frame, kernel, sigma):
    return cv2.GaussianBlur(frame, kernel, sigma)

def blurBilateral(frame, sigma):
    return cv2.bilateralFilter(frame, 9, sigma, sigma)

# Gaussian filter find the Gaussian weighted avg in the neighbourhood pixels, inot taking into account their intensity, and it blurs the edges.
# In bilateral filter, only pixels with similar intensities to the central pixel are considered for blurring, resulting in preserved edges
# (bc of large intensity variation).

# 1.3
def grabHSV(frame):
    lower = np.array([90, 50, 50])
    upper = np.array([130, 255, 255])
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
        
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
    mask_1_bgr = cv2.cvtColor(closing-mask, cv2.COLOR_GRAY2BGR)
    mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = (255, 0, 0)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    mask_morph = cv2.add(mask, mask_1_bgr)

    return mask_morph

def grabRGB(frame):
    lower = np.array([110, 70, 60])
    upper = np.array([255, 160, 100])

    mask = cv2.inRange(frame, lower, upper)
        
    kernel = np.ones((11, 11), np.uint8)
    dilatation = cv2.dilate(mask, kernel=kernel, iterations=1)
    closing = cv2.morphologyEx(dilatation, cv2.MORPH_CLOSE, kernel)
    # closing = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
    mask_1_bgr = cv2.cvtColor(closing-mask, cv2.COLOR_GRAY2BGR)
    mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = (255, 0, 0)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    mask_morph = cv2.add(mask, mask_1_bgr)

    return mask_morph

# 2.1
def sobel(frame, ddepth, dxy, ksize):
    # dxy - first, second, or third derivative; ksize - 1,3,5,7; ddepth - output image depth (same as source)
    blur = cv2.GaussianBlur(frame, (3, 3), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    sobelx = cv2.Sobel(src=gray, ddepth=ddepth, dx=dxy, dy=0, ksize=ksize)
    sobely = cv2.Sobel(src=gray, ddepth=ddepth, dx=0, dy=dxy, ksize=ksize)

    _, sobelx = cv2.threshold(sobelx, 70, 255, 0)
    mask_x = cv2.cvtColor(sobelx, cv2.COLOR_GRAY2BGR)
    mask_x[np.where((mask_x==[255, 255, 255]).all(axis=2))] = (255, 0, 255)
    _, sobely = cv2.threshold(sobely, 70, 255, 0)
    mask_y = cv2.cvtColor(sobely, cv2.COLOR_GRAY2BGR)
    mask_y[np.where((mask_y==[255, 255, 255]).all(axis=2))] = (255, 255, 0)

    return cv2.add(mask_x, mask_y)

# 2.2
def hough(frame, method, dp, minDist, param1, param2, minRadius=0, maxRadius=0):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 1.5)

    # circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=70, param2=70, minRadius=0, maxRadius=0)
    circles = cv2.HoughCircles(img, method, dp, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    # method - HOUGH_GRADIENT, HOUGH_GRADIENT_ALT; dp - inverse ratio of the accumulator resolution, 1.5 for ALT
    # minDist - inimum distance between the centers of the detected circles.

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for c in circles[0, :]:
            cv2.circle(frame, (c[0], c[1]), c[2], (255, 255, 0), 4)
            # cv2.circle(frame, (c[0], c[1]), 1, (255, 0, 255), 5)
    
    return frame

# 2.3
def makeTemplate(frame):
    crop = None
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 1.5)
    h, w, _ = frame.shape

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.5, 10, param1=100, param2=100, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))

        chosen = circles[0, :][0]
        for c in circles[0, :][1:]:
            if c[0] > chosen[0]:
                chosen = c
        c = chosen
        if c[0] > w*0.75:
            cv2.rectangle(frame, (c[0]-c[2], c[1]-c[2]), (c[0]+c[2], c[1]+c[2]), color=(255, 0, 0), thickness=5)
            crop = frame[c[1]-c[2]:c[1]+c[2], c[0]-c[2]:c[0]+c[2]]

    return frame, crop

def matchTemplate(frame, t):
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    width, height = image_gray.shape[::-1]
    res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    res = cv2.resize(res, (width, height), interpolation=cv2.INTER_LINEAR)
    res=((res-np.min(res))/(np.max(res)-np.min(res))*255).astype("uint8")
    return res

def draw(frame, prevMask=None):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_yellow = np.array([20, 100, 10])
    upper_yellow = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel=kernel)
    mask = cv2.dilate(mask, kernel=kernel)
    
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        # cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 255), 3)
        cv2.circle(mask, (int(x), int(y)), int(r), (255, 255, 255), -1)
    
    if prevMask is None:
        prevMask = mask

    mask = cv2.add(mask, prevMask)
    prevMask = mask

    mask_1_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = (0, 255, 255)

    mask_morph = cv2.add(frame, mask_1_bgr)

    return mask_morph, prevMask

def dyeMask(frame, mask, color):
    mask_1_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = color

    mask_morph = cv2.add(frame, mask_1_bgr)
    return mask_morph

def writeText(frame, text, x=50, y=50, color=(0,0,0)):
    wrapped_text = textwrap.wrap(text, width=65)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1.5
    font_thickness = 2

    textsize = cv2.getTextSize(wrapped_text[0], font, font_size, font_thickness)[0]
    gap = textsize[1] + 15

    for line in wrapped_text:
        y += gap
        x = x

        cv2.putText(frame, line, (x, y), font, font_size, color, font_thickness, lineType = cv2.LINE_AA)

    return frame