import cv2
from ultralytics import YOLO

# Load YOLOv8 nano model (fast)
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame)

    phone_found = False

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]

            # Check for phone
            if label == "cell phone":
                phone_found = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2),
                              (0, 0, 255), 2)

                cv2.putText(frame, "PHONE DETECTED",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 0, 255), 2)

    # Status text
    if phone_found:
        cv2.putText(frame, "📵 PHONE DETECTED",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    else:
        cv2.putText(frame, "✅ NO PHONE",
                    (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 3)

    cv2.imshow("Phone Detection - YOLO", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
