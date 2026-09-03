import cv2
import time

URL = "http://100.76.102.158:4747/video"
cap = cv2.VideoCapture(URL)

lower = (90, 120, 120)
higher = (130, 255, 255)

frame_count = 0
totals = {"capture": 0, "hsv": 0, "mask": 0, "contours": 0}

while True:
    t0 = time.perf_counter()
    ret, frame = cap.read()
    t1 = time.perf_counter()

    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    t2 = time.perf_counter()

    mask = cv2.inRange(hsv, lower, higher)
    t3 = time.perf_counter()

    contours, _ =cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    t4 = time.perf_counter()

    totals["capture"] += (t1 - t0) * 1000
    totals["hsv"] += (t2 - t1) * 1000
    totals["mask"] += (t3 - t2) * 1000
    totals["contours"] += (t4 - t3) * 1000
    frame_count +=1

    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"\nAveraged over {frame_count} frames:")
for stage, total in totals.items():
    print(f"{stage}: {total / frame_count:.2f}ms avg")