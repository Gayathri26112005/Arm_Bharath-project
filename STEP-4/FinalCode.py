Gesture_media_control:

import cv2
import mediapipe as mp
import pyautogui
import time

# -------------------- MediaPipe setup --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# -------------------- Camera --------------------
cap = cv2.VideoCapture(0)

# -------------------- State variables --------------------
last_action_time = 0
ACTION_DELAY = 1.2
is_playing = False
gesture_text = "No Hand"

# -------------------- Finger counting --------------------
def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    count = 0

    # Thumb
    if lm[17].x < lm[5].x:  # Right hand
        if lm[4].x > lm[3].x:
            count += 1
    else:  # Left hand
        if lm[4].x < lm[3].x:
            count += 1

    # Other fingers
    tips = [8, 12, 16, 20]
    for tip in tips:
        if lm[tip].y < lm[tip - 2].y:
            count += 1

    return count

# -------------------- Main loop --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    finger_count = -1

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            finger_count = fingers_up(hand)

            current_time = time.time()

            # ---------------- Gesture Labels ----------------
            if finger_count == 0:
                gesture_text = "PAUSE"
            elif finger_count == 1:
                gesture_text = "PLAY"
            elif finger_count == 2:
                gesture_text = "VOLUME UP"
            elif finger_count == 3:
                gesture_text = "VOLUME DOWN"
            elif finger_count == 4:
                gesture_text = "FORWARD"
            elif finger_count == 5:
                gesture_text = "BACKWARD"
            else:
                gesture_text = "UNKNOWN"

            # ---------------- Gesture Actions ----------------
            if current_time - last_action_time > ACTION_DELAY:

                # PAUSE
                if finger_count == 0 and is_playing:
                    pyautogui.press('space')
                    is_playing = False
                    last_action_time = current_time

                # PLAY
                elif finger_count == 1 and not is_playing:
                    pyautogui.press('space')
                    is_playing = True
                    last_action_time = current_time

                elif finger_count == 2:
                    pyautogui.press('up')
                    last_action_time = current_time

                elif finger_count == 3:
                    pyautogui.press('down')
                    last_action_time = current_time

                elif finger_count == 4:
                    pyautogui.press('right')
                    last_action_time = current_time

                elif finger_count == 5:
                    pyautogui.press('left')
                    last_action_time = current_time

    else:
        gesture_text = "No Hand"

    # ---------------- Display ----------------
    cv2.putText(frame, f"Gesture: {gesture_text}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Fingers: {finger_count}", (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    status = "PLAYING" if is_playing else "PAUSED"
    cv2.putText(frame, f"Status: {status}", (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 255), 2)

    cv2.imshow("Gesture Media Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- Cleanup ----------------
cap.release()
cv2.destroyAllWindows()
