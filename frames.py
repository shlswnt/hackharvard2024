import cv2
import threading
import signal
import sys
import numpy as np
from collections import deque
from ultralytics import YOLO
import math
import csv
from datetime import datetime

dict_of_urls = {
    "Vegas": [
        "https://d1wse4.its.nv.gov:443/vegasxcd04/73c2fe7c-2f08-43d4-bca5-e43e7fca737c_lvflirxcd06_public.stream/playlist.m3u8",
    ]
}

# Local server URL
video_url = dict_of_urls["Vegas"][0]

# Create a VideoCapture object
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a deque to store frames (buffer)
frame_buffer = deque()

# Create a lock for the buffer
buffer_lock = threading.Lock()

# Store vehicle bounding boxes and their states for the last 15 frames
vehicle_history = deque(maxlen=15)
vehicle_states = {}

# Create a lock for the vehicle history
vehicle_history_lock = threading.Lock()

# Threshold for "too close" (in pixels)
distance_threshold = 50

# Line position (y-coordinate) for counting vehicles
line_position = 150

# Initialize car and truck counters
car_count = 0
truck_count = 0
count = 0

# Log start time when the program starts
start_time = datetime.now()

# Function to capture frames in a separate thread
def capture_frames():
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        i += 1
        if i % 2 == 0:
            i = 0
            continue
        with buffer_lock:
            frame_buffer.append(frame)
            print(f"Buffer size: {len(frame_buffer)}")
        
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break
    

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    cap.release()
    cv2.destroyAllWindows()
    end_time = datetime.now()
    
    # Save the final count to CSV
    with open('vehicle_count.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([start_time, end_time, car_count, truck_count])

    sys.exit(0)

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Function to calculate Euclidean distance between two points
def calculate_distance(box1, box2):
    center1 = ((box1[0] + box1[2]) // 2, (box1[1] + box1[3]) // 2)
    center2 = ((box2[0] + box2[2]) // 2, (box2[1] + box2[3]) // 2)
    return math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2)

def process_frames():
    global car_count, truck_count, count
    model = YOLO('yolov8s.pt')
    while True:
        frames = []
        with buffer_lock:
            if len(frame_buffer) >= 5:
                # Take 5 frames at once
                for _ in range(1):
                    frames.append(frame_buffer.popleft())

        if not frames:
            continue

        # Process each frame
        for frame in frames:
            # Object detection
            results = model(frame)

            detections = []

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
                    label = int(box.cls)
                    confidence = float(box.conf)

                    # Only consider cars (class_id 2) and trucks (class_id 7) in YOLOv8
                    if label in [2, 7]:  
                        detections.append([x1, y1, x2, y2, confidence, label])

            # Draw the counting line
            cv2.line(frame, (0, line_position), (frame.shape[1], line_position), (0, 0, 255), 2)

            # Compare detections to vehicle history
            with vehicle_history_lock:
                count += 1
                if count % 60 == 0:
                    count = 0
                    vehicle_states.clear()
                    vehicle_history.clear()
                for detection in detections:
                    x1, y1, x2, y2, confidence, class_id = detection
                    track_id = f"{class_id}_{x1}_{y1}_{x2}_{y2}"
                    if track_id not in vehicle_states:
                        vehicle_states[track_id] = {'counted': False}
                    if y1 < line_position < y2:
                        too_close = False
                        for previous_box in vehicle_history:
                            if calculate_distance(previous_box, [x1, y1, x2, y2]) < distance_threshold:
                                too_close = True
                                break
                        if not too_close and not vehicle_states[track_id]['counted']:
                            vehicle_states[track_id]['counted'] = True
                            vehicle_history.append([x1, y1, x2, y2])
                            if class_id == 2:
                                car_count += 1
                            elif class_id == 7:
                                truck_count += 1
                            print(f"Car Count: {car_count}, Truck Count: {truck_count}")


def start_threads(num_threads=3):
    for _ in range(num_threads):
        thread = threading.Thread(target=process_frames)
        thread.daemon = True
        thread.start()

# Initialize CSV file with headers
with open('vehicle_count.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Start Time', 'End Time', 'Car Count', 'Truck Count'])

# Start the threads
start_threads()

capture_frames()

# Cleanup
cap.release()
cv2.destroyAllWindows()
