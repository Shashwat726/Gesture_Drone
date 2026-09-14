import cv2
import math
import mediapipe as mp
from collections import deque, Counter
from mediapipe.tasks.python import vision
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python.vision import hand_landmarker

URL = "http://100.104.194.46:4747/video"

base_options = mp_python.BaseOptions(model_asset_path = 'hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options)

wrist_history = deque(maxlen = 10)
index_history = deque(maxlen=40)
gesture_buffer = deque(maxlen = 10)
smoothed_wrist_y = None
stable_gesture = "HOVER"

def is_finger_up(hand_landmarks, tip_id):
    
    palm_length = get_distance(hand_landmarks[9], hand_landmarks[0])
    
    tip_to_wrist = get_distance(hand_landmarks[tip_id], hand_landmarks[0])
    
    threshold = 1.3
    
    return tip_to_wrist > (palm_length * threshold)

def get_distance(lm1, lm2):
    return math.sqrt((lm1.x - lm2.x)**2 + (lm1.y - lm2.y)**2)

cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks, handedness in zip(result.hand_landmarks, result.handedness):
            drawing_utils.draw_landmarks(frame, hand_landmarks, hand_landmarker.HandLandmarksConnections.HAND_CONNECTIONS)

            hand_label = handedness[0].category_name

            thumb_up = is_finger_up(hand_landmarks, 4)
            index_up = is_finger_up(hand_landmarks, 8)
            middle_up = is_finger_up(hand_landmarks, 12)
            ring_up = is_finger_up(hand_landmarks, 16)
            pinky_up = is_finger_up(hand_landmarks, 20)

            finger_states = [thumb_up, index_up, middle_up, ring_up, pinky_up]

            raw_y = hand_landmarks[0].y

            if smoothed_wrist_y is None:
                smoothed_wrist_y = raw_y
            else:
                smoothed_wrist_y = (0.3 * raw_y) + (0.7 * smoothed_wrist_y)

            wrist_history.append(smoothed_wrist_y)

            detected_gesture = "HOVER"
            
            thumb_index_dist = get_distance(hand_landmarks[4], hand_landmarks[8])
            thumb_middle_dist = get_distance(hand_landmarks[4], hand_landmarks[12])
            
            palm_length = get_distance(hand_landmarks[9], hand_landmarks[0])
            pinch_threshold = palm_length * 0.25
            
            thumb_index_dist = get_distance(hand_landmarks[4], hand_landmarks[8])
            thumb_middle_dist = get_distance(hand_landmarks[4], hand_landmarks[12])

            if thumb_index_dist < pinch_threshold and thumb_middle_dist < pinch_threshold and pinky_up:
                detected_gesture = "VIDEO (Record)"
            elif thumb_index_dist < pinch_threshold and pinky_up:
                detected_gesture = "PHOTO (Snap)"

                
            elif finger_states == [True, True, True, True, True] and len(wrist_history) == 10:
                y_movement = wrist_history[0] - wrist_history[-1] 
                if y_movement > 0.02:
                    detected_gesture = "ARISE"
                elif y_movement < -0.02:
                    detected_gesture = "LAND"
                else:
                    detected_gesture = "OPEN_HAND (Hover)"

            
            elif finger_states == [False, True, False, False, False]: 

                index_history.append((hand_landmarks[8].x, hand_landmarks[8].y))
                
                if len(index_history) == 40:
                    xs = [p[0] for p in index_history]
                    ys = [p[1] for p in index_history]

                    width = max(xs) - min(xs)
                    height = max(ys) - min(ys)

                    if width > 0.15 and height > 0.15 and 0.5 < (width / height) < 2.0:

                        start_p = index_history[0]
                        end_p = index_history[-1]
                        loop_dist = math.sqrt((start_p[0] - end_p[0])**2 + (start_p[1] - end_p[1])**2)
                        
                        if loop_dist < 0.1:
                            detected_gesture = "360 ORBIT !!!"
                        else:
                            detected_gesture = "POINT (Drawing...)"
                    else:
                        detected_gesture = "POINT"
            
            elif finger_states == [False, False, False, False, False]:
                index_history.clear()
                

                fist_x = hand_landmarks[9].x 
                fist_y = hand_landmarks[9].y
                
                dx = fist_x - 0.5 
                dy = fist_y - 0.5 

                detected_gesture = f"FIST LOCK (X:{dx:.2f}, Y:{dy:.2f})"
            
            else:
                index_history.clear()

            gesture_buffer.append(detected_gesture)

            if len(gesture_buffer) == 10:
                counts = Counter(gesture_buffer)
                most_common_gesture, count = counts.most_common(1)[0]

                if count >= 7:
                    stable_gesture = most_common_gesture
            
        cv2.putText(frame, f"CMD: {stable_gesture}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

        cv2.imshow("Final Gestures", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()    