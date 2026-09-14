import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python as mp_python

# 1. Import the modern Tasks API drawing utilities
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python.vision import hand_landmarker

LANDMARK_NAMES = {
    0: "WRIST",
    1: "THUMB_CMC",  2: "THUMB_MCP",   3: "THUMB_IP",    4: "THUMB_TIP",
    5: "INDEX_MCP",  6: "INDEX_PIP",   7: "INDEX_DIP",   8: "INDEX_TIP",
    9: "MIDDLE_MCP", 10: "MIDDLE_PIP", 11: "MIDDLE_DIP", 12: "MIDDLE_TIP",
    13: "RING_MCP",  14: "RING_PIP",   15: "RING_DIP",   16: "RING_TIP",
    17: "PINKY_MCP", 18: "PINKY_PIP",  19: "PINKY_DIP",  20: "PINKY_TIP" 
}

base_options = mp_python.BaseOptions(model_asset_path='hand_landmarker.task')

# 2. Configure confidence thresholds
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

# 3. Connect to Phone Feed
URL = "http://100.76.67.121:4747/video"
cap = cv2.VideoCapture(URL)

def is_finger_up(hand_landmarks, tip_id, pip_id):
    if hand_landmarks[tip_id].y < hand_landmarks[pip_id].y:
        return True
    else:
        return False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame dropped")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

    result = detector.detect(mp_image)

    # 4. Draw the landmarks cleanly
    if result.hand_landmarks:
        for hand_landmarks in result.hand_landmarks:
            # We can now pass the hand_landmarks list directly! No conversion needed.
            drawing_utils.draw_landmarks(
                frame,
                hand_landmarks,
                hand_landmarker.HandLandmarksConnections.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style()
            )
            # Day 23:{ Extracting Landmark Coordinates
            #     h, w, _ = frame.shape
            
            # # 2. Extract specific landmarks by their index number
            # # 0 = Wrist, 8 = Index fingertip
            # wrist = hand_landmarks[0]
            # index_tip = hand_landmarks[8]
            
            # # 3. Convert normalized coordinates (0.0 - 1.0) to actual pixel coordinates
            # wrist_x, wrist_y = int(wrist.x * w), int(wrist.y * h)
            # index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)
            
            # # 4. Print them live to the console
            # print(f"Wrist: ({wrist_x}, {wrist_y}) | Index Tip: ({index_x}, {index_y})")
            
            # # 5. Draw manual circles on these specific points
            # cv2.circle(frame, (wrist_x, wrist_y), 15, (0, 255, 0), cv2.FILLED) # Green circle on wrist
            # cv2.circle(frame, (index_x, index_y), 15, (255, 0, 0), cv2.FILLED) # Blue circle on index tip
            # }

            #Day 24:{ 21 points named
            # h, w, _ = frame.shape
            # console_output = ""

            # for idx, landmark in enumerate(hand_landmarks):
            #     cx, cy = int(landmark.x * w), int(landmark.y * h)
            #     name = LANDMARK_NAMES[idx]

            #     cv2.putText(frame, name, (cx + 5, cy), cv2.FONT_HERSHEY_PLAIN, 0.7, (0, 255, 0), 1)

            #     console_output += f"{idx}: ({cx}, {cy})"

            # print(console_output)}

            index_up = is_finger_up(hand_landmarks, 8,6)
            middle_up = is_finger_up(hand_landmarks, 12, 10)
            ring_up = is_finger_up(hand_landmarks, 16, 14)
            pinky_up = is_finger_up(hand_landmarks, 20, 18)

            thumb_up = hand_landmarks[4].x > hand_landmarks[1].x

            finger_states = [thumb_up, index_up, middle_up, ring_up, pinky_up]

            binary_states = [1 if state else 0 for state in finger_states]
            state_text = f"Fingers: {binary_states}"
            cv2.putText(frame, state_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            print(state_text)
            
    cv2.imshow("Hand Detection - Live Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()