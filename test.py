from ultralytics import YOLO
import cv2
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 150)

model = YOLO("yolov8n.pt")
cap   = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    img = model(frame)

    for i in img:
        img2 = i.plot()
        cv2.imshow("TASHINGA", img2)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
