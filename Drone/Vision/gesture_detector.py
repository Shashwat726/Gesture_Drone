import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python.vision import hand_landmarker

URL = "http://100.76.67.121:4747/video"

base_options = mp_python.BaseOptions(model_asset_path = 'hand_landmarker.task')
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)
stable_gesture = "NONE"
current_gesture = "NONE"
gesture_frame_count = 0

def is_finger_up(hand_landmarks, tip_id, pip_id):
    return hand_landmarks[tip_id].y < hand_landmarks[pip_id].y

cap = cv2.VideoCapture(URL)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame_rgb)
    result = detector.detect(mp_image)

    if result.hand_landmarks:
        for hand_landmarks, handedness in zip(result.hand_landmarks, result.handedness):
            drawing_utils.draw_landmarks(
                frame, hand_landmarks,
                hand_landmarker.HandLandmarksConnections.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style()
            )
            hand_label = handedness[0].category_name

            index_up = is_finger_up(hand_landmarks, 8, 6)
            middle_up = is_finger_up(hand_landmarks, 12, 10)
            ring_up = is_finger_up(hand_landmarks, 16, 14)
            pinky_up = is_finger_up(hand_landmarks, 20, 18)
            
                        # Hardcoded for your specific right-hand camera setup!
            thumb_up = hand_landmarks[4].x < hand_landmarks[3].x
                
            finger_states = [thumb_up, index_up, middle_up, ring_up, pinky_up]
            
            detected_gesture = "NONE"
            if finger_states == [True, True, True, True, True]:
                detected_gesture = "OPEN_HAND"
            elif finger_states == [False, False, False, False, False]:
                detected_gesture = "FIST"
            
            if detected_gesture == current_gesture:
                gesture_frame_count += 1
            else:
                current_gesture = detected_gesture
                gesture_frame_count = 0
                
            if gesture_frame_count >= 5:
                stable_gesture = current_gesture
            
            cv2.putText(frame, f"Gesture: {stable_gesture}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    cv2.imshow("Drone Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
