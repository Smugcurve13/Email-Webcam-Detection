import cv2 as cv
import time
import glob
from send_mail import send_email

video = cv.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count =1
while True:
    status = 0
    check , frame = video.read()
    grey_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    grey_frame_gau = cv.GaussianBlur(grey_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = grey_frame_gau

    delta_frame = cv.absdiff(first_frame, grey_frame_gau)

    thresh_frame = cv.threshold(delta_frame, 60, 255, cv.THRESH_BINARY)[1]
    dilFrame = cv.dilate(thresh_frame, None, iterations=2)
    cv.imshow("my video", dilFrame)

    contours, check = cv.findContours(dilFrame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv.contourArea(contour) < 5000:
            continue
        x,y,w,h = cv.boundingRect(contour)
        rectangle = cv.rectangle(frame,(x,y),(x+w, y+h), (0,255,0), 3)
        if rectangle.any:
            status = 1
            cv.imwrite(f'images/{count}.png',frame)
            count = count +1
            all_images = glob.glob('images/*.png')
            index = int(len(all_images)/2)
            image_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0]==1 and status_list[1]==0:
        send_email(image_with_object)

    print(status_list)

    cv.imshow('video',frame) 
    key = cv.waitKey(1)

    if key == ord('q'):
        break

video.release()