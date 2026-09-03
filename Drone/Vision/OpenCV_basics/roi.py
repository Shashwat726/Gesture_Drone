import cv2

URL = "http://100.81.74.169:4747/video"
cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape
    x1, y1 = width // 4, height // 4
    x2, y2 = (3 * width) // 4, (3 * height) // 4

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    roi = frame[y1:y2 , x1:x2]

    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    lower = (90, 120, 120)
    higher = (130, 255, 255)
    mask = cv2.inRange(hsv_roi, lower, higher)

    # print(frame.shape)
    # print(roi.shape)

    cv2.imshow("Original", frame)
    cv2.imshow("Region of Interest", roi)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()