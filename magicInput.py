import time, cv2, mediapipe
from trackingModule import handDetector
import math

#fist, L, ok, surfer dude (positions)
#swpie left, swipe right (movement) (choose between different control states)
#Different gestures to go to volume, input, and cursor control
#All in one document, with an open gesture and close gesture (and sleep after 2 minutes)


tipIDs = [4, 8, 12, 16, 20]

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    fingers = []
    total = int
    while True:
        success, img = cap.read()
        detector = handDetector()
        img2 = detector.findHands(img)
        lmList = detector.findPosition(img2)
        if len(lmList) != 0:
            if lmList[tipIDs[0]][1] > lmList[tipIDs[0]-1][1]:
                fingers.append(1)  # 1 means open
            else:
                fingers.append(0)
            for id in range(1, 5):
                if lmList[tipIDs[id]][2] < lmList[tipIDs[id]-2][2]:
                    fingers.append(1)  # 1 means open
                else:
                    fingers.append(0)
            total = fingers.count(1)

        print(total)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img2, f"FPS: {str(int(fps))}", (15, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 182, 18), 1)
        cv2.putText(img2, f"Input: {str(total)}", (15, 130), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 182, 18), 1)

        cv2.imshow("Image", img2)
        cv2.waitKey(1)

        total = 0
        fingers = []

main()