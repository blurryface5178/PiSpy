import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.createTrackbar('MedianBlur (2n+1)','Trackbars',0,15,nothing)
cv2.createTrackbar('BilateralThreshold Min','Trackbars',0,50,nothing)
cv2.createTrackbar('BilateralThreshold Max','Trackbars',100,400,nothing)
cv2.createTrackbar('Threshold Min','Trackbars',216,255,nothing)
cv2.createTrackbar('Threshold Max','Trackbars',255,255,nothing)
frame = cv2.VideoCapture(0)

while True:
    _, image = frame.read()
    image_GRAY = cv2.cvtColor(image,
                              cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.medianBlur(image_GRAY,
                                   cv2.getTrackbarPos('MedianBlur (2n+1)','Trackbars')*2+1,
                                   0)
    filtered_image = cv2.bilateralFilter(blurred_image,
                                         cv2.getTrackbarPos('BilateralThreshold Min','Trackbars'),
                                         cv2.getTrackbarPos('BilateralThreshold Max','Trackbars'),
                                         1)
    _, thresholded = cv2.threshold(filtered_image,
                                   cv2.getTrackbarPos('Threshold Min', 'Trackbars'),
                                   cv2.getTrackbarPos('Threshold Max', 'Trackbars'),
                                   0)
    cv2.imshow('Output',thresholded)

    if cv2.waitKey(1)==27:
        break

frame.release()
cv2.destroyAllWindows()