import cv2

URL = "http://100.109.213.12:4747/video"
cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

    lower = (90,50,50)
    higher = (130, 255, 255)
    
    mask = cv2.inRange(hsv, lower, higher)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)
    cv2.imshow("Original", frame)
    cv2.imshow("HSV", hsv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()