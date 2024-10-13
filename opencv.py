import cv2
import threading
import signal
import sys
from collections import deque
from ultralytics import YOLO

# Video URL
video_url = "https://d1wse4.its.nv.gov:443/vegasxcd04/73c2fe7c-2f08-43d4-bca5-e43e7fca737c_lvflirxcd06_public.stream/playlist.m3u8"

# Create a VideoCapture object
cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Create a deque to store frames (buffer)
frame_buffer = deque()

# Create a lock for the buffer
buffer_lock = threading.Lock()

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Function to detect vehicles (as defined above)
def detect_vehicles(frame):
    # Run inference
    results = model(frame)
    
    # Process results
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Get box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw rectangle
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Optionally, add label and confidence
            conf = box.conf[0]
            cls = int(box.cls[0])
            label = f'{model.names[cls]} {conf:.2f}'
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

# Function to capture frames in a separate thread
def capture_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        # Perform vehicle detection on the frame
        processed_frame = detect_vehicles(frame)
        # Append the processed frame to the buffer
        with buffer_lock:
            frame_buffer.append(processed_frame)
            # print(f"Buffer size: {len(frame_buffer)}")

# Start the frame capture thread
thread = threading.Thread(target=capture_frames, daemon=True)
thread.start()

def signal_handler(sig, frame):
    print('Exiting gracefully...')
    cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

while True:
    with buffer_lock:
        if len(frame_buffer) > 50:
            # Display a frame from 5 seconds ago (the oldest frame in the buffer)
            frame_to_display = frame_buffer[0]  # The oldest frame in the buffer
            # Remove it from the buffer
            frame_buffer.popleft()
            cv2.imshow('Video Stream with YOLOv8 Vehicle Detection', frame_to_display)

    # Check for key press to exit
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()