import cv2

URL = "http://100.73.208.119:4747/video"
cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (5,5), 0)

    lower = (90, 120, 120)
    higher = (130, 255, 255)
    mask = cv2.inRange(hsv, lower, higher)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = frame.copy()
    # cv2.drawContours(output, contours, -1, (0,255,0), 2)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:
            continue

        x,y,w,h = cv2.boundingRect(cnt)

        cv2.rectangle(output, (x,y), (x+w, y+h), (255, 0, 0), 2)

        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)

    cv2.imshow("Contours", output)
    cv2.imshow("Mask", mask)
    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()