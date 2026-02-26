import cv2
from ultralytics import YOLO
import serial
import time

# ==============================
# CHANGE COM PORT HERE
# ==============================
esp = serial.Serial('COM3', 9600)
time.sleep(2)

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

phone_detected_prev = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    phone_detected = False

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            if label == "cell phone":
                phone_detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 0, 255), 2)

                cv2.putText(frame, "PHONE DETECTED",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)

    # Send signal to ESP32
    if phone_detected and not phone_detected_prev:
        esp.write(b'1')   # move servo
        phone_detected_prev = True

    if not phone_detected and phone_detected_prev:
        esp.write(b'0')   # reset servo
        phone_detected_prev = False

    # Display status
    if phone_detected:
        cv2.putText(frame, "📵 PHONE DETECTED",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    else:
        cv2.putText(frame, "✅ NO PHONE",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)

    cv2.imshow("YOLO Phone Detection + ESP32", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
esp.close()
cv2.destroyAllWindows()
