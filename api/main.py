import cv2
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ultralytics import YOLO

# Globals
app = FastAPI()
model = YOLO('yolov8n.pt')

with open("../preprocess/results.json", "r") as data_json:
    data = json.load(data_json)

with open("../preprocess/cities.json", "r") as cities_json:
    cities = json.load(cities_json)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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

@app.get('/')
def hello_world():
    return {"Hello": "World"}

@app.get('/get_all_names/')
def get_intersection_names():
    return list(data.keys())

@app.get('/get_all_cities/')
def get_city_names():
    return list(cities.keys())

@app.get("/video/")
def get_frames(name: str):
    video_url = data[name]["video_url"]
    if not video_url:
        raise HTTPException(status_code=404, detail="Video does not exist for this intersection")
    if not video_url.endswith(".m3u8"):
        raise HTTPException(status_code=404, detail="Invalid video format")
    else:
        return StreamingResponse(generate_frames(video_url), media_type="multipart/x-mixed-replace; boundary=frame")
    
@app.get("/intersection/")
def get_intersection_score(name: str):
    return data[name]

@app.get("/city/")
def get_intersection_in_city(name: str):
    return cities[name]