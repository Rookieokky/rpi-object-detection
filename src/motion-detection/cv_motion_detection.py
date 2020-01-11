"""
Detect any motion in the frame.

<Author>
Xiaotian Dai
YunFei Robotics Labrotary
http://www.xiaotiandai.com/
"""

import cv2
import time
import numpy as np

cnt_frame = 0

# create video capture
cam = cv2.VideoCapture(0)


def mse(image_a, image_b):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


try:
    while True:
        # record start time
        start = time.time()

        # Read the frames from a camera
        _, frame = cam.read()

        # Convert to gray image
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find edges
        edges = cv2.Canny(frame_gray,100,200)

        # Show the original and processed image
        cv2.imshow('gray', frame_gray)
        cv2.imshow('edge', edges)

        # Calculate MSE
        if cnt_frame > 0:
            if mse(frame_gray, frame_gray_p) > 100:
                print('Frame{0}: Motion Detected!'.format(cnt_frame))

        # if key pressed is 'Esc' then exit the loop
        if cv2.waitKey(1)== 27:
            break

        # record end time
        end = time.time()

        # calculate FPS
        seconds = end - start
        fps = 1.0 / seconds
        # print("Estimated fps:{0:0.1f}".format(fps));

        cnt_frame = cnt_frame + 1
        edges_p = edges
        frame_gray_p = frame_gray

finally:
    # Clean up and exit the program
    cv2.destroyAllWindows()
    cam.release()
