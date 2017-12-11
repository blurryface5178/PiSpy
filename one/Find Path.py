import numpy as np
import cv2
from matplotlib import pyplot as plt

capture = cv2.VideoCapture(0)

while True:
    if cv2.waitKey(1) == 27:
        break

    # Capture frame-by-frame
    isOpen, frame = capture.read()

    if isOpen:  # if camera is open
        # (Our operations on the frame come here)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Converting to ColorSpace HSV

        low_limit = np.array([0, 0, 0])  # Setting lower and upper limit to mask
        max_limit = np.array([245, 155, 155])

        masked_frame = cv2.inRange(frame, low_limit, max_limit)  # Applying mask

        masked_frame = cv2.medianBlur(masked_frame, 15, 0)
        masked_frame = cv2.bilateralFilter(masked_frame, 30, 200, 1)

        cv2.imshow('Showing', frame)
        cv2.imshow('Result', masked_frame)

        # print("Masking Successful")

    else:
        print("No camera available")
        break

capture.release()  # When everything done, releasing the capture
cv2.destroyAllWindows()
