import cv2

URL = "http://100.76.102.158:4747/video"
cap = cv2.VideoCapture(URL)

backSub = cv2.createBackgroundSubtractorMOG2(history = 500, varThreshold = 16, detectShadows = True)
prev_gray = None

while True:
    ret, frame = cap.read()
    if not ret: 
        break

    fg_mask = backSub.apply(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 
    if prev_gray is not None:
        diff = cv2.absdiff(gray, prev_gray)
        cv2.imshow("Frame Diff", diff)
    cv2.imshow("Original", frame)
    cv2.imshow("Foreground Mask", fg_mask)

    prev_gray = gray.copy()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()