import cv2
import mediapipe as mp
import serial
import time

ser = serial.Serial('COM3',115200)  # change port
time.sleep(2)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:

            # simple detection example
            # if fingers folded → fist

            wrist = handLms.landmark[0]
            tip = handLms.landmark[8]

            if tip.y > wrist.y:
                print("FIST")
                ser.write(b'F')

            else:
                print("HIGH FIVE")
                ser.write(b'H')

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hand",img)

    if cv2.waitKey(1) & 0xFF == 27:
        break