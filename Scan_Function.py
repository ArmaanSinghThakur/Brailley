import cv2
import numpy as np
from pyzbar.pyzbar import decode


cap= cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4, 480)


def Scan():
    run= True
    while run:
        success, img = cap.read()
        for barcode in decode(img):
            code = barcode.data.decode("utf-8")
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            if code:
                return code
                run = False
        cv2.imshow("Result", img)
        cv2.waitKey(1)





