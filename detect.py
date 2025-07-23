from ultralytics import YOLO
import cv2
from gtts import gTTS
from playsound import playsound
import time
import os
import threading

# Load YOLO model
model = YOLO("yolov8n.pt")

#speak an introduction to my project
text = "hie welcome to my project"

tts = gTTS(text=text,lang='en')
filename1 = "intro.mp3"
tts.save(filename1)
playsound(filename1)
os.remove(filename1)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Time control
speak_interval = 3  # seconds
last_spoken_time = 0
is_speaking = False

# Speak function in background

def speak(text):
    def run():
        global is_speaking
        is_speaking = True
        tts = gTTS(text=text, lang='en')
        filename = "temp_speech.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
        is_speaking = False
    threading.Thread(target=run, daemon=True).start()

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, stream=True)

    for r in results:
        annotated_frame = r.plot()
        boxes = r.boxes
        names = r.names

        spoken_objects = []

        for box in boxes:
            cls = int(box.cls[0])
            label = names[cls]
            x1, y1, x2, y2 = box.xyxy[0]
            height = y2 - y1
            distance = 1000 / float(height) if height > 0 else 0
            distance = round(distance, 1)
            spoken_objects.append(f"{label} about {distance} units away")

        current_time = time.time()
        if spoken_objects and (current_time - last_spoken_time > speak_interval) and not is_speaking:
            message = "I see " + ", ".join(spoken_objects)
            print(message)
            speak(message)
            last_spoken_time = current_time

        cv2.imshow("Tashinga Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
