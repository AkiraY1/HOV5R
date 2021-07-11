import time, cv2, mediapipe
from trackingModule import handDetector
import math

#All in one document, connected
#Sleep too
#off state

tipIDs = [4, 8, 12, 16, 20]

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    fingers = []
    total = int
    activeList = []
    endList = []

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

            #start
            if (lmList[4][1] > lmList[2][1]) and (total == 1):
                activeList.append(1)
                if activeList[-25:-1].count(1) == 24:
                    print("start")
                    break
            else:
                activeList.append(0)

            #end
            #if total == 0:
            #    endList.append(1)
            #    if endList[-25:-1].count(1) == 24:
            #        print("end")
            #        break
            #else:
            #    endList.append(0)

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