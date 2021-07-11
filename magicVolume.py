import cv2
import mediapipe as mp
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from trackingModule import handDetector

#Distance
#Position
#Depth

class volumeControl():
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    def getVolume(self):
        currentVolumeDb = self.volume.GetMasterVolumeLevel()
        return currentVolumeDb

    def getRange(self):
        volumeRange = self.volume.GetVolumeRange()
        return volumeRange

    def setVolume(self, vr):
        self.volume.SetMasterVolumeLevel(vr, None)


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    v = volumeControl()
    range = v.getRange()
    prev_distance = 100
    while True:
        success, img = cap.read()
        detector = handDetector()
        img2 = detector.findHands(img)
        lmList = detector.findPosition(img2)
        if len(lmList) != 0:
            #print(lmList[4], lmList[8])
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

            distance = math.hypot(x2 - x1, y2 - y1)
            print(distance)
            
            if distance > prev_distance:
                try:
                    v.setVolume(v.getVolume()+1)
                except:
                    pass
                print("increase")
            
            if distance < prev_distance:
                try:
                    v.setVolume(v.getVolume()-1)
                except:
                    pass
                print("increase")
            
            prev_distance = distance
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img2, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img2)
        cv2.waitKey(1)

main()

#v = volumeControl()
#print(v.getVolume())
#print(v.getRange()[2])
#v.setVolume(-62.98)
