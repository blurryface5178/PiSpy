# Mike Shinoda:
# Have I been lost all along?
# Was there something I could say or something I should not have done?
# Was I lost all along?
# Was I looking for an answer when there never really was one?

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


def find_distance(a, b):
    [x1, y1] = a
    [x2, y2] = b
    dist = math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))
    return dist


def find_matching_contour(contours_video):
    text = ""
    x, y = [], []

    ret = [cv2.matchShapes(contours_image[1], contours_video[i], 1, 0.0) for i in range(len(contours_video))]
    min_ret_index = ret.index(min(ret))

    out = cv2.drawContours(img, contours_video, min_ret_index, (150, 250, 50), 5)

    if cv2.contourArea(contours_video[min_ret_index]) > 15000:
        print (cv2.contourArea(contours_video[min_ret_index]))
        error = 0.01 * cv2.arcLength(contours_video[min_ret_index], True)
        approx_poly = cv2.approxPolyDP(contours_video[min_ret_index], error, True)

        for points in approx_poly:
            [[a, b]] = points
            x.append(a)
            y.append(b)

        right_most = [max(x), y[x.index(max(x))]]
        left_most = [min(x), y[x.index(min(x))]]
        top_most = [x[y.index(max(y))], max(y)]
        bottom_most = [x[y.index(min(y))], min(y)]

        dist_1 = find_distance(right_most, top_most)
        dist_2 = find_distance(right_most, bottom_most)
        dist_3 = find_distance(left_most, top_most)
        dist_4 = find_distance(left_most, bottom_most)

        if (dist_1 > dist_3 and dist_2 > dist_4):
            text = 'Left'
        elif (dist_1 < dist_3 and dist_2 < dist_4):
            text = 'Right'

        draw_approx = cv2.drawContours(out, approx_poly, -1, (255, 255, 255), 5)

        return [text, draw_approx]
    else:
        return['No Match', img]


img = cv2.imread('arrow.jpg')
image_image, contours_image, hierarchy_image = return_contours(img)

frame = cv2.VideoCapture(0)

while True:
    if cv2.waitKey(1) == 27:
        break

    _, img = frame.read()
    image_video, contours_video, hierarchy_video = return_contours(img)

    if len(contours_video) != 0:
        text, matched_contour = find_matching_contour(contours_video)
        cv2.putText(matched_contour, "{:}".format(text), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (150, 105, 255), 2, cv2.LINE_AA)
        cv2.imshow('Approx', matched_contour)

frame.release()
cv2.destroyAllWindows()