import cv2
import numpy as np

URL = "http://100.81.74.169:4747/video"
cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    lower = (90, 120, 120)
    higher = (130, 255, 255)
    
    mask = cv2.inRange(hsv, lower, higher)
    kernel = np.ones((5, 5), np.uint8)
    eroded = cv2.erode(mask, kernel, iterations = 1)
    dilated = cv2.dilate(mask, kernel, iterations = 1)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    

    cv2.imshow("Original", frame)
    cv2.imshow("HSV", hsv)
    cv2.imshow("Mask", mask)
    cv2.imshow("Eroded", eroded)
    cv2.imshow("Dilated", dilated)
    cv2.imshow("Opening", opening)
    cv2.imshow("Closing", closing)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()