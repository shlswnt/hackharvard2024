import cv2
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from ultralytics import YOLO

# Globals
app = FastAPI()
model = YOLO('yolov8n.pt')

with open("../preprocess/results.json", "r") as input_json:
    data = json.load(input_json)


# Helper Functions

def detect_vehicles(frame):
    results = model(frame)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            conf = box.conf[0]
            cls = int(box.cls[0])
            label = f'{model.names[cls]} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def generate_frames(video_url):
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="Could not open video stream")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Perform vehicle detection
        processed_frame = detect_vehicles(frame)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()


# Routes

@app.get("/video/")
def get_frames(video_url: str):
    if video_url.endswith(".m3u8"):
        return StreamingResponse(generate_frames(video_url), media_type="multipart/x-mixed-replace; boundary=frame")
    else:
        raise HTTPException(status_code=404, detail="Invalid video format")
    
@app.get("/intersection/")
def get_intersection_score(intersection_name: str):
    return data[intersection_name]