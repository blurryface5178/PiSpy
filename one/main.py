import cv2
import numpy as np
import math

def return_contours(img):
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    masked_frame = cv2.medianBlur(img2, 15, 0)
    masked_frame = cv2.bilateralFilter(img2, 30, 200, 1)
    _, thresh2 = cv2.threshold(masked_frame, 127, 255, 0)
    cv2.imshow('Output', thresh2)
    return cv2.findContours(thresh2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

def return_value(image_index):
    ret = [cv2.matchShapes(contours_image[0], contours_video[i], 1, 0.0) for i in range(len(contours_video))]
    min_ret_index = ret.index(min(ret))
    minimum_value = min(ret)
    out = cv2.drawContours(img, contours_video, min_ret_index, (150, 250, 50), 5)
    return [minimum_value,cv2.contourArea(contours_video[min_ret_index])]

def find_matching_contour(contours_video):
    x, y = [], []
    text = 0

    val1,area1=return_value(0)
    val2, area2= return_value(1)

    text=val1+val2
    tot_area = area1+area2

    if tot_area > 1000 and text<8:
        return ['Logo Vetiyo Hai?', img]
    else:
        return['Khai kei vetena ta', img]


img = cv2.imread('tech_plain.jpg')
image_image, contours_image, hierarchy_image = return_contours(img)

frame = cv2.VideoCapture(0)

while True:
    if cv2.waitKey(1) == 27:
        break

    _, img = frame.read()
    image_video, contours_video, hierarchy_video = return_contours(img)

    if len(contours_video) != 0:
        text, matched_contour = find_matching_contour(contours_video)
        cv2.putText(matched_contour, "{:}".format(text), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 150, 250), 2, cv2.LINE_AA)
        cv2.imshow('Approx', matched_contour)

    cv2.imshow('Logo', cv2.drawContours(cv2.imread('tech_plain.jpg'), contours_image, -1, (150, 250, 50), 5))

frame.release()
cv2.destroyAllWindows()