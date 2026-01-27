import cv2
import mediapipe as mp
import serial
import time

# 🔧 CHANGE THIS TO YOUR ESP32 PORT
SERIAL_PORT = 'COM3'      # Linux: '/dev/ttyUSB0'
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

last_state = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    mouth_open = False

    if result.multi_face_landmarks:
        for face in result.multi_face_landmarks:
            upper_lip = face.landmark[13].y
            lower_lip = face.landmark[14].y

            if (lower_lip - upper_lip) > 0.03:
                mouth_open = True

    # Send data only if state changes
    if mouth_open and last_state != "open":
        ser.write(b'1')
        last_state = "open"
    elif not mouth_open and last_state != "closed":
        ser.write(b'0')
        last_state = "closed"

    status_text = "MOUTH OPEN 😮" if mouth_open else "MOUTH CLOSED 😐"
    color = (0, 255, 0) if mouth_open else (0, 0, 255)

    cv2.putText(frame, status_text, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.imshow("Mouth Controlled Servo", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
ser.close()

