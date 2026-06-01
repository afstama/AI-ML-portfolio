"""Skeleton code for python script to process a video using OpenCV package

:copyright: (c) 2021, Joeri Nicolaes
:license: BSD license
"""
import argparse
import cv2
import sys
from frame import *


# helper function to change what you do based on video seconds
def between(cap, lower: int, upper: int) -> bool:
    return lower <= int(cap.get(cv2.CAP_PROP_POS_MSEC)) < upper


def main(input_video_file: str, output_video_file: str) -> None:
    # OpenCV video objects to work with
    cap = cv2.VideoCapture(input_video_file)
    fps = int(round(cap.get(5)))
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')        # saving output video as .mp4
    out = cv2.VideoWriter(output_video_file, fourcc, fps, (frame_width, frame_height))
    prevMask = None
    hardTemp = None


    # while loop where the real work happens
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if cv2.waitKey(28) & 0xFF == ord('q'):
                break
            if between(cap, 0, 500) or between(cap, 900, 1400) or between(cap, 1800, 2300) or between(cap, 2600, 3000) or between(cap, 3400, 3900):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            if between(cap, 0, 4000):
                writeText(frame, 'Grayscale.')

            if between(cap, 4000, 5500):
                frame = cv2.GaussianBlur(frame, (5, 5), 0)
                writeText(frame, 'Gaussian blur; kernel=(5,5);  wider kernel = stronger blur.')
            if between(cap, 5500, 7000):
                frame = cv2.GaussianBlur(frame, (11, 11), 0)
                writeText(frame, 'Gaussian blur; kernel=(11,11);  wider kernel = stronger blur.')
            if between(cap, 7000, 8000):
                frame = cv2.GaussianBlur(frame, (21, 21), 0)
                writeText(frame, 'Gaussian blur; kernel=(21,21);  wider kernel = stronger blur.')
            if between(cap, 8000, 9000):
                frame = cv2.bilateralFilter(frame, 9, 50, 50)
                writeText(frame, 'Bilateral filter; d=9, sigmaColor=50, sigmaSpace=50;  larger sigmaColor = stronger blur, larger sigmaSpace = more cartoonish.')
            if between(cap, 9000, 10000):
                frame = cv2.bilateralFilter(frame, 9, 450, 50)
                writeText(frame, 'Bilateral filter; d=9, sigmaColor=450, sigmaSpace=50;  larger sigmaColor = stronger blur, larger sigmaSpace = more cartoonish.')
            if between(cap, 10000, 11000):
                frame = cv2.bilateralFilter(frame, 9, 50, 450)
                writeText(frame, 'Bilateral filter; d=9, sigmaColor=50, sigmaSpace=450;  larger sigmaColor = stronger blur, larger sigmaSpace = more cartoonish.')
            if between(cap, 11000, 12000):
                frame = cv2.bilateralFilter(frame, 9, 450, 450)
                writeText(frame, 'Bilateral filter; sigmaColor=450, sigmaSpace=450;  larger sigmaColor = stronger blur, larger sigmaSpace = more cartoonish.')
            if between(cap, 4000, 12000):
                writeText(frame, 'Gaussian filter - weighted average of neighbour pixels, does not take into account their intensity, and it blurrs the edges; Bilateral filter - only pixels with similar intensities to the central are considered for blurring, resulting in preserved edges.', y=150)
            
            if between(cap, 12000, 16000):
                frame = grabRGB(frame)
                writeText(frame, 'Grabbing blue objects using the RGB range (white) and improving by dilatation and closing (blue).', color=(255,255,255))
            if between(cap, 16000, 20000):
                frame = grabHSV(frame)
                writeText(frame, 'Grabbing blue objects using the HSV range (white) and improving by closing twice (blue).', color=(255,255,255))

            if between(cap, 20000, 21250):
                frame = sobel(frame, -1, 1, 5)
                writeText(frame, 'Sobel; first derivative, ksize=5 (horizontal edges are blue, vertical are purple) - more detected edges, but also more noise.', color=(255,255,255))
            if between(cap, 21250, 22500):
                frame = sobel(frame, -1, 2, 5)
                writeText(frame, 'Sobel; second derivative, ksize=5 (horizontal edges are blue, vertical are purple) - more detected edges and less noise.', color=(255,255,255))
            if between(cap, 22500, 23750):
                frame = sobel(frame, -1, 2, 7)
                writeText(frame, 'Sobel; second derivative, ksize=7 (horizontal edges are blue, vertical are purple) - a lot detected edges and a lot of noise, edges are detected where there aren\'t any.', color=(255,255,255))
            if between(cap, 23750, 25000):
                frame = sobel(frame, -1, 1, 3)
                writeText(frame, 'Sobel; first derivative, ksize=3 (horizontal edges are blue, vertical are purple) - less detected edges, but they are more bold, and no noise.', color=(255,255,255))
            
            if between(cap, 25000, 26500):
                frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1, 10, 60, 0.9)
                writeText(frame, 'Hough; GRADIENT_ALT, dp=1, minDist=10, param1=60, param2=0.9 - some patterns detected as circles, along with the actual circular objects.')
            if between(cap, 26500, 28000):
                frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 10, 60, 0.9)
                writeText(frame, 'Hough; GRADIENT_ALT, dp=1.5, minDist=10, param1=60, param2=0.9 - a bit more smaller patterns detected as circles, along with the actual circular objects.')
            if between(cap, 28000, 29500):
                frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 10, 20, 0.5)
                writeText(frame, 'Hough; GRADIENT_ALT, dp=1.5, minDist=10, param1=20, param2=0.5 - high sensitivity, a lot of patterns detected as circles, circular objects detected as multiple circles.')
            if between(cap, 29500, 31000):
                frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 70, 60, 0.9)
                writeText(frame, 'Hough; GRADIENT_ALT, dp=1.5, minDist=70, param1=60, param2=0.9 - good detection, with some smaller circles.')
            if between(cap, 31000, 32500):
                frame = hough(frame, cv2.HOUGH_GRADIENT_ALT, 1.5, 70, 100, 0.9)
                writeText(frame, 'Hough; GRADIENT_ALT, dp=1.5, minDist=70, param1=100, param2=0.9 - good detection, with less smaller circles.')
            if between(cap, 32500, 34000):
                frame = hough(frame, cv2.HOUGH_GRADIENT, 1.5, 10, 100, 100)
                writeText(frame, 'Hough; GRADIENT, dp=1.5, minDist=10, param1=100, param2=100 - a lot of close circles, but some nonexistent circles detected too.')
            if between(cap, 34000, 35500):
                frame = hough(frame, cv2.HOUGH_GRADIENT, 1.5, 50, 90, 100)
                writeText(frame, 'Hough; GRADIENT, dp=1.5, minDist=50, param1=90, param2=100 - good detection, but objects detected as multiple circles.')
            
            if between(cap, 35500, 38500):
                frame, temp = makeTemplate(frame)
                if temp is not None:
                    hardTemp = temp
                writeText(frame, 'Grabbing the ball using HoughCircles (method=HOUGH_GRADIENT, dp=1.5, minDist=10, param1=100, param2=100), drawing a rectangle using the ball coordinates and radius and making a template by cutting the frame.')
            if between(cap, 38500, 43000):
                frame = matchTemplate(frame, hardTemp)
                writeText(frame, 'Template matching using TM_CCOEFF_NORMED.')

            if between(cap, 43000, 57000):
                frame, prevMask = draw(frame, prevMask)
                writeText(frame, 'Drawing in space by grabbing the yellow tip of the marker, contouring it and transforming into a circle. Saving the previous mask and adding the current mask of the marker tip, then applying the whole mask to the frame.')
            if between(cap, 57000, 57100) or between(cap, 57200, 57300) or between(cap, 57400, 57500) or between(cap, 57600, 57700) or between(cap, 57800, 57900) or between(cap, 58000, 58100) or between(cap, 58200, 58300) or between(cap, 58400, 58500) or between(cap, 58600, 58700) or between(cap, 58800, 58900) or between(cap, 59000, 59100) or between(cap, 59200, 59300) or between(cap, 59400, 59500) or between(cap, 59600, 59700) or between(cap, 59800, 59900):
                frame = dyeMask(frame, prevMask, (0, 255, 255))
            if between(cap, 57000, 59900):
                writeText(frame, 'Making the drawing disappear by alternating between frames with and without the mask.')
            if between(cap, 59900, 61000):
                writeText(frame, 'Thanks for watching. Bye!')
            
            if int(cap.get(cv2.CAP_PROP_POS_MSEC)) > 61000:
                break

            # ...

            # write frame that you processed to output
            out.write(frame)

            # (optional) display the resulting frame
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture and writing object
    cap.release()
    out.release()
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenCV video processing')
    parser.add_argument('-i', "--input", help='full path to input video that will be processed')
    parser.add_argument('-o', "--output", help='full path for saving processed video output')
    args = parser.parse_args()

    if args.input is None or args.output is None:
        sys.exit("Please provide path to input and output video files! See --help")

    main(args.input, args.output)
    # main("C:\\Users\\afs\\Documents\\8sem\\ComputerVision\\assignment1\\inputVid.mp4",
    #      "C:\\Users\\afs\\Documents\\8sem\\ComputerVision\\assignment1\\outputVid.mp4")
