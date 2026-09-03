import cv2

URL = "http://100.73.208.119:4747/video"
cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret_val, simple_thresh = cv2.threshold(gray, 127, 225, cv2.THRESH_BINARY)

    ret_val, otsu_thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    adaptive_thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    cv2.imshow("Original", frame)
    cv2.imshow("Gray", gray)
    cv2.imshow("Simple Threshold", simple_thresh)
    cv2.imshow("Otsu Threshold", otsu_thresh)
    cv2.imshow("Adaptive Threshold", adaptive_thresh)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()