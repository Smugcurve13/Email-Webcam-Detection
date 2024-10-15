import cv2 as cv
import time

video = cv.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:
    check , frame = video.read()
    grey_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    grey_frame_gau = cv.GaussianBlur(grey_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = grey_frame_gau

    delta_frame = cv.absdiff(first_frame, grey_frame_gau)
    cv.imshow("my video", delta_frame)

    key = cv.waitKey(1)

    if key == ord('q'):
        break

video.release()