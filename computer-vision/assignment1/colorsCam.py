import numpy as np
import cv2
import matplotlib.pyplot as plt


def hsvCam():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # hue sat value

        # purple
        # lower = np.array([130, 100, 100])
        # upper = np.array([170, 255, 255])

        # blue
        # lower = np.array([90, 50, 50])
        # upper = np.array([130, 255, 255])

        # green
        lower = np.array([40, 40, 40])
        upper = np.array([80, 255, 255])

        # red
        # lower = np.array([0, 50, 50])
        # upper = np.array([10, 255, 255])

        mask = cv2.inRange(hsv, lower, upper)
        
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask_1_bgr = cv2.cvtColor(closing-mask, cv2.COLOR_GRAY2BGR)
        mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = (0, 0, 255)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        mask_morph = cv2.add(mask, mask_1_bgr)

        res = cv2.bitwise_and(frame, frame, mask=closing)

        # cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask_1_bgr)
        # cv2.imshow('closing', closing)
        cv2.imshow('morphology', mask_morph)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


def rgbCam():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        
        # blue
        lower = np.array([100, 0, 0])
        upper = np.array([255, 100, 100])
        mask = cv2.inRange(frame, lower, upper)
        
        kernel = np.ones((11, 11), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask_1_bgr = cv2.cvtColor(closing-mask, cv2.COLOR_GRAY2BGR)
        mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = (0, 0, 255)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        mask_morph = cv2.add(mask, mask_1_bgr)

        res = cv2.bitwise_and(frame, frame, mask=closing)

        # cv2.imshow('frame', frame)
        # cv2.imshow('mask', mask_1_bgr)
        # cv2.imshow('closing', closing)
        cv2.imshow('morphology', mask_morph)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


def sobel():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        sobelx = cv2.Sobel(src=gray, ddepth=-1, dx=1, dy=0, ksize=3)
        sobely = cv2.Sobel(src=gray, ddepth=-1, dx=0, dy=1, ksize=3)

        _, sobelx = cv2.threshold(sobelx, 70, 255, 0)
        mask_x = cv2.cvtColor(sobelx, cv2.COLOR_GRAY2BGR)
        mask_x[np.where((mask_x==[255, 255, 255]).all(axis=2))] = (255, 0, 255)
        _, sobely = cv2.threshold(sobely, 70, 255, 0)
        mask_y = cv2.cvtColor(sobely, cv2.COLOR_GRAY2BGR)
        mask_y[np.where((mask_y==[255, 255, 255]).all(axis=2))] = (255, 255, 0)

        res = cv2.add(mask_x, mask_y)
        # res = cv2.add(res, mask_y)

        cv2.imshow('frame', res)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    cap.release()


def hough():
    cap = cv2.VideoCapture(0)
    
    while True:
        _, frame = cap.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (7, 7), 1.5)

        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=70, param2=70, minRadius=0, maxRadius=0)

        if circles is not None:
            circles = np.uint16(np.around(circles))

            for c in circles[0, :]:
                cv2.circle(frame, (c[0], c[1]), c[2], (0, 255, 0), 3)
                cv2.circle(frame, (c[0], c[1]), 1, (0, 0, 255), 5)
        

        cv2.imshow('frame', frame)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows() 
    cap.release()


def makeTemplate(frame):
    crop = frame
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (7, 7), 1.5)

    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=70, param2=70, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))

        c = circles[0, :][1]
        # cv2.rectangle(frame, (c[0]-c[2], c[1]-c[2]), (c[0]+c[2], c[1]+c[2]), color=(255, 0, 0), thickness=2)
        crop = frame[c[1]-c[2]:c[1]+c[2], c[0]-c[2]:c[0]+c[2]]

    return crop 

def matchTemplate(frame, template):
    image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
    
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(frame, top_left, bottom_right, 255, 2)
    
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(frame,cmap = 'gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle(meth)
 
    # plt.show()

    cv2.imshow('frame', frame)
    cv2.imshow('intensity', res)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# frame = cv2.imread('objects.png')
# template = makeTemplate(frame)
# matchTemplate(frame, template)
    

def draw():
    cap = cv2.VideoCapture(0)
    prevMask = None

    while True:
        _, frame = cap.read()
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
            cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 255), 3)
            cv2.circle(mask, (int(x), int(y)), int(r), (255, 255, 255), -1)
        
        if prevMask is None:
            prevMask = mask
            print('first')

        mask = cv2.add(mask, prevMask)
        prevMask = mask

        mask_1_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        mask_1_bgr[np.where((mask_1_bgr==[255, 255, 255]).all(axis=2))] = (0, 255, 255)

        mask_morph = cv2.add(frame, mask_1_bgr)


        # res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', mask_morph)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    
    cv2.destroyAllWindows()
    cap.read



def mouseRGB(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        colorsB = frame[y,x,0]
        colorsG = frame[y,x,1]
        colorsR = frame[y,x,2]
        colors = frame[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BRG Format: ",colors)
        print("Coordinates of pixel: X: ",x,"Y: ",y)


cv2.namedWindow('mouseRGB')
cv2.setMouseCallback('mouseRGB',mouseRGB)

capture = cv2.VideoCapture("C:\\Users\\afs\\Documents\\8sem\\ComputerVision\\assignment1\\inputVidSmall.mp4")

while(True):

    ret, frame = capture.read()

    cv2.imshow('mouseRGB', frame)

    if cv2.waitKey(1) == 27:
        break

capture.release()
cv2.destroyAllWindows()