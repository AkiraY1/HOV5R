from tkinter import *
from typing import Sized
from tkinter_custom_button import TkinterCustomButton
from PIL import ImageTk, Image
import time, cv2, mediapipe
from trackingModule import handDetector
import math, pyautogui
from volumeControl import volumeControl

#----------------------------------------------------------------------------------------------------------------------------------------
#Finger tip IDs
tipIDs = [4, 8, 12, 16, 20]

#Counts fingers
def fingerCount(fingers, lmList):
    if lmList[tipIDs[0]][1] > lmList[tipIDs[0]-1][1]:
        fingers.append(1)
    else:
        fingers.append(0)
    for id in range(1, 5):
        if lmList[tipIDs[id]][2] < lmList[tipIDs[id]-2][2]:
            fingers.append(1)
        else:
            fingers.append(0)
    total = fingers.count(1)
    return total

#Input numbers
def input():
    state_display.configure(text = "Input")
    state_display.update()

    cap = cv2.VideoCapture(0)

    fingers = []
    total = int
    activeList = []
    endList = []
    prev_x = 320

    while True:
        success, img = cap.read()
        detector = handDetector()
        img2 = detector.findHands(img)
        lmList = detector.findPosition(img2)
        if len(lmList) != 0:
            #Counting fingers
            total = fingerCount(fingers, lmList)

            print(total)

            # SwitchState
            if total == 5:
                if lmList[12][1] > (prev_x+100):
                    print("right")
                    vvol()
                if lmList[12][1] < (prev_x-100):
                    print("left")
                    cursor()
            prev_x = lmList[12][1]

            #sleep
            if total == 0:
                endList.append(1)
                if endList[-25:-1].count(1) == 24:
                    print("sleeping")
                    sleep()
            else:
                endList.append(0)
        cv2.waitKey(1)

        total = 0
        fingers = []

#Volume
def vvol():
    state_display.configure(text = "Volume")
    state_display.update()

    cap = cv2.VideoCapture(0)
    v = volumeControl()
    prev_distance = 100

    fingers = []
    total = int
    activeList = []
    endList = []
    prev_x = 320

    while True:
        success, img = cap.read()
        detector = handDetector()
        img2 = detector.findHands(img)
        lmList = detector.findPosition(img2)
        if len(lmList) != 0:

            #Counting fingers
            total = fingerCount(fingers, lmList)

            #print(lmList[4], lmList[8])
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

            #Volume Control
            distance = math.hypot(x2 - x1, y2 - y1)            
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

            # SwitchState
            if total == 5:
                if lmList[12][1] > (prev_x+100):
                    print("right")
                    cursor()
                if lmList[12][1] < (prev_x-100):
                    print("left")
                    input()
            prev_x = lmList[12][1]

            #sleep
            if total == 0:
                endList.append(1)
                if endList[-25:-1].count(1) == 24:
                    print("sleeping")
                    sleep()
            else:
                endList.append(0)
        cv2.waitKey(1)

        total = 0
        fingers = []

#Cursor
def cursor():
    state_display.configure(text = "Cursor")
    state_display.update()

    cap = cv2.VideoCapture(0)

    fingers = []
    total = int
    activeList = []
    endList = []
    prev_x = 320

    while True:
        success, img = cap.read()
        detector = handDetector()
        img2 = detector.findHands(img)
        lmList = detector.findPosition(img2)
        if len(lmList) != 0:

            #Counting fingers
            total = fingerCount(fingers, lmList)

            #CursorMove
            x, y = lmList[8][1], lmList[8][2]
            xp, yp = ((640-x)/500), (y/250)
            x0, y0 = (xp*1920), (yp*1080)
            x1, y1 = lmList[12][1], lmList[12][2]
            distance = math.hypot(x - x1, y - y1)
            x2, y2 = lmList[4][1], lmList[4][2]
            distance2 = math.hypot(x - x2, y - y2)
            pyautogui.moveTo(x0, y0)

            #CursorScroll
            if distance2 < 40:
                if y2 > 200:
                    pyautogui.scroll(-60)
                if y2 < 200:
                    pyautogui.scroll(60)

            #CursorClick
            if distance < 25:
                pyautogui.click()

            # SwitchState
            if total == 5:
                if lmList[12][1] > (prev_x+100):
                    print("right")
                    input()
                if lmList[12][1] < (prev_x-100):
                    print("left")
                    vvol()
            prev_x = lmList[12][1]

            #sleep
            if total == 0:
                endList.append(1)
                if endList[-25:-1].count(1) == 24:
                    print("sleeping")
                    sleep()
            else:
                endList.append(0)
        cv2.waitKey(1)

        total = 0
        fingers = []

#Sleeping, must activate DONE
def sleep():
    state_display.configure(text = "Sleep")
    state_display.update()

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

            #Counting fingers
            total = fingerCount(fingers, lmList)

            #activate
            if (lmList[4][1] > lmList[2][1]) and (total == 1):
                activeList.append(1)
                if activeList[-25:-1].count(1) == 24:
                    print("activated")
                    cursor()
            else:
                activeList.append(0)

            #end application
            if total == 0:
                endList.append(1)
                if endList[-31:-1].count(1) == 30:
                    state_display.configure(text = "OFF")
                    state_display.update()
                    print("ended")
                    break
            else:
                endList.append(0)
        cv2.waitKey(1)

        total = 0
        fingers = []

#-----------------------------------------------------------------------------------------------------------------------------------------

def power():
    print("Power Pressed")
    sleep()

window = Tk()
window.title("HOV5R")
window.geometry("140x100")
window.configure(bg="#E7F0FF")

photo = ImageTk.PhotoImage(Image.open("C:\\Users\\Akira\\Desktop\\Code\\magictouch\\src\\images\\touchy.jpg"))
window.iconphoto(False, photo)

button_1 = TkinterCustomButton(text="Power", corner_radius=20, command=power, width=100, height=40, hover_color="#4392F1", fg_color="#DC493A", text_font="Calibri")
button_1.place(relx=0.5, rely=0.1, anchor='n')
bvalue = "Start"

state_display = Label(window, text="OFF", bg="#E7F0FF")
state_display.config(font=("Calibri", 12))
state_display.place(relx = 0.5, rely = 0.9, anchor ='s')

window.mainloop()