import cv2
import time
import numpy as np

URL = "http://100.109.67.230:4747/video"
cap = cv2.VideoCapture(URL)

lower = (90, 120, 120)
higher = (130, 255, 255)

kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
    mask = cv2.inRange(hsv, lower, higher)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ =cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = frame.copy()

    if contours:
        largest = max(contours, key = cv2.contourArea)
        area = cv2.contourArea(largest)
        
        if area > 500:
            x, y, w, h = cv2.boundingRect(largest)
            cv2.rectangle(output, (x, y), (x + w, y + h), (255, 0, 0), 2)

            M = cv2.moments(largest)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)
                cv2.putText(output, f"X: {cx}, Y: {cy}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
    cv2.imshow("Original", frame)
    cv2.imshow("Processed", output)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()