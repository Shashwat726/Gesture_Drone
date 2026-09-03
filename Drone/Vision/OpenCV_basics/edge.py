import cv2

URL = "http://100.81.74.169:4747/video"
cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges_raw = cv2.Canny(gray, 100, 200)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges_blurred = cv2.Canny(blur, 100, 200)

    cv2.imshow("Original", frame)
    cv2.imshow("Gray", gray)
    cv2.imshow("Canny_no_blur", edges_raw)
    cv2.imshow("Canny_blurred", edges_blurred)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()