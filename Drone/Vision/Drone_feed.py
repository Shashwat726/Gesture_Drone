import cv2
import time
import os
from datetime import datetime

URL = "http://100.82.14.18:4747/video"
os.makedirs("Captures/snapshots", exist_ok=True)
os.makedirs("Captures/recordings", exist_ok=True)

def connent_stream(url):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Failed to connect stream")
        return None
    print("Stream connected")
    return cap

def read_frame(cap):
    ret, frame = cap.read()
    if not ret:
        return None
    return frame

def display_frame(frame, fps):
    h, w, _ = frame.shape
    center_x, center_y = w//2, h//2

    #Border
    cv2.rectangle(frame, (10, 10), (w-10, h-10), (255, 0, 0), 2)

    #Crosshair
    cv2.line(frame, (center_x - 30, center_y), (center_x + 30, center_y), (0, 255, 0), 2)
    cv2.line(frame, (center_x, center_y - 30), (center_x, center_y + 30), (0, 255, 0), 2)

    #Circle
    cv2.circle(frame, (center_x, center_y), 10, (0, 0, 255), 2)

    #FPS
    cv2.putText(frame, f"FPS: {int(fps)}", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Drone Feed", frame)

def cleanup(cap):
    cap.release()
    cv2.destroyAllWindows()
    print("Cleanup Done")

def main():
    cap = connent_stream(URL)
    if cap is None:
        return

    prev_time = 0
    recording = False
    out = None

    while True:
        frame = read_frame(cap)

        if frame is None:
            print("Frame lost, attempting reconnect...")
            cap = connent_stream(URL)
            continue

        curr_time = time.time()
        fps = 1/ (curr_time - prev_time)
        prev_time = curr_time

        if recording:
            out.write(frame)

        display_frame(frame, fps)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

        elif key == ord('s'):
            filename = "Captures/Snapshots/" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            cv2.imwrite(filename, frame)
            print("Snapshot saved.")

        elif key == ord('r'):

            if not recording:
                h, w, _ = frame.shape
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                filename = "Captures/Recordings/" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".avi"
                out = cv2.VideoWriter(filename, fourcc, 20, (w, h))
                recording = True
                print("Recording started")
            else:
                recording = False
                out.release()
                print("Recording saved")

    if recording and out:
        out.release()

    cleanup(cap)

if __name__ == "__main__":
    main()