import cv2
import mediapipe as mp
import time
import math
from pynput.mouse import Button, Controller
import pyautogui
from trackingModule import handDetector

#Distance
#Position
#Depth

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        detector = handDetector()
        img2 = detector.findHands(img)
        lmList = detector.findPosition(img2)
        if len(lmList) != 0:
            x, y = lmList[8][1], lmList[8][2]
            xp, yp = ((640-x)/640), (y/400)-0.1
            x0, y0 = (xp*1920), (yp*1080)

            x1, y1 = lmList[12][1], lmList[12][2]
            distance = math.hypot(x - x1, y - y1)

            x2, y2 = lmList[4][1], lmList[4][2]
            distance2 = math.hypot(x - x2, y - y2)

            pyautogui.moveTo(x0, y0)

            if distance2 < 40:
                if y2 > 200:
                    pyautogui.scroll(-60)
                if y2 < 200:
                    pyautogui.scroll(60)

            if distance < 25:
                pyautogui.click()
            
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img2, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img2)
        cv2.waitKey(1)

main()
