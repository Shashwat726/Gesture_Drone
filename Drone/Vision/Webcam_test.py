import cv2
import time

cap = cv2.VideoCapture("http://100.85.200.50:4747/video")

prev_time = 0
recording = False
out = None

while(True):
    ret,frame = cap.read()
    h, w, _ = frame.shape
    center_x, center_y = w//2, h//2
    if not ret:
        print("Failed to grab frame")
        break
    if recording:
        out.write(frame)


    curr_time = time.time()
    fps = 1/(curr_time - prev_time)
    prev_time = curr_time

    # Border rectangle
    cv2.rectangle(frame, (10,10), (w-10, h-10), (0, 255, 0), 2)

    # Crosshair
    cv2.line(frame, (center_x - 30, center_y), (center_x + 30, center_y), (0, 255, 0), 2)
    cv2.line(frame, (center_x, center_y - 30), (center_x, center_y + 30), (0, 255, 0), 2)

    # Circle at center
    cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), 2)

    #FPS Text
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Phone Feed", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('s'):
        cv2.imwrite("snapshot.jpg",frame)
        print("Snapshot saved")
    elif key == ord('r'):
        if not recording:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('recording.avi', fourcc, 20, (w, h))
            recording = True
            print("Recording Started")
        else:
            recording = False
            out.release()
            print("Recording saved")

cap.release()
cv2.destroyAllWindows()