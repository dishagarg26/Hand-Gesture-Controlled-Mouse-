import cv2
import mediapipe as mp
import pyautogui
import numpy as np

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1)
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Index finger tip
                    cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)

                if id == 4:  # Thumb tip
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y
                    if abs(index_y - thumb_y) < 50:
                        pyautogui.click()
                        pyautogui.sleep(1)

    cv2.imshow("Hand Mouse", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
