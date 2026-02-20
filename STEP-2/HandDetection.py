Run the below lines in bash (Linux):

pip3 install mediapipe
pip3 install opencv-python


Run this below code in a file which is created in linux:

import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        fingers = detector.fingersUp(hands[0])
        print(fingers)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
