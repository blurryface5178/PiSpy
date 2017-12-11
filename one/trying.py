import cv2
import numpy as np

cascade1 = cv2.CascadeClassifier('superman.xml')

frame = cv2.VideoCapture(0)

while True:
    if cv2.waitKey(1) == 27:
       break
    _, from_video = frame.read()
    gray = cv2.cvtColor(from_video,cv2.COLOR_BGR2GRAY)

    logo = cascade1.detectMultiScale(gray,1.1,5)
    for (x, y, w, h) in logo:
        from_video = cv2.rectangle(from_video, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = from_video[y:y + h, x:x + w]

    cv2.imshow('img', from_video)
    cv2.imshow('img_gray', gray)


cv2.destroyAllWindows()