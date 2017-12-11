import cv2
import numpy as np

image_name = ['x thingy.png', 'superman.png', 'tech.jpg']

def nothing(x):
    pass

def standard_deviation(matches,key1,key2):
    distances = []

    for match in matches:
        photo_index = match.queryIdx
        thresholded_index = match.trainIdx

        (x1, y1) = key1[photo_index].pt
        (x2, y2) = key2[thresholded_index].pt

        distances.append(calcDist(x1, y1, x2, y2))

    n = len(matches)
    tot_dist = sum(distances)
    average = tot_dist / n

    differences = []
    for distance in distances:
        difference = distance - average
        differences.append(difference ** 2)

    tot_diff = sum(differences)
    std_dev = (tot_diff / (n - 1)) ** .5

    return std_dev


def calcDist(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**.5


def threshold(image):
    image_GRAY = cv2.cvtColor(image,
                              cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.medianBlur(image_GRAY,11)
    _, thresholded = cv2.threshold(blurred_image,175,255,0)
    return thresholded

def detectAndShow(image_index):
    img3 = np.ones((640, 480))
    matches = bf.match(des1[image_index], des2)

    if len(matches)>0:
        matches = sorted(matches, key=lambda x: x.distance)
        img3 = cv2.drawMatches(photos[image_index], key1[image_index], thresholded, key2, matches[:10], img3, flags=2)
        error = standard_deviation(matches, key1[image_index],key2)
    else:
        error = 0

    cv2.putText(img3, '{:}'.format(error), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
    cv2.imshow('Matches'+str(image_index),img3)

    return error


error_list = []

frame = cv2.VideoCapture(0)

key1 , des1, photos = [],[],[]
orb = cv2.ORB_create()

for image in image_name:
    photo = cv2.imread(image)
    photo = threshold(photo)
    key, des = orb.detectAndCompute(photo, None)
    key1.append(key)
    des1.append(des)
    photos.append(photo)

while True:
    _, image = frame.read()
    thresholded = threshold(image)
    cv2.imshow('Output',thresholded)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    key2, des2 = orb.detectAndCompute(thresholded,None)

    for i in range(3):
        error = detectAndShow(i)

    if cv2.waitKey(1) == 27:
        error_list.append(error)
        print('Appended')
        break

print(error_list)
print(error_list.index(min(error_list)))

frame.release()
cv2.destroyAllWindows()