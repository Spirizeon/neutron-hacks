from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
import random
import json
import time
import os

app = Flask(__name__)

# Initialize Faster R-CNN model with Detectron2
def initialize_frcnn_model():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cpu"  # Set to "cuda" if GPU is available
    return DefaultPredictor(cfg)

predictor = initialize_frcnn_model()

# Function to process each frame of the video feed
def process_frame(frame):
    outputs = predictor(frame)
    detections = outputs["instances"].to("cpu")
    
    # Draw bounding boxes around detected objects
    degraded_frame = frame.copy()
    for i in range(len(detections)):
        bbox = detections.pred_boxes[i].tensor.numpy().astype(int)[0]
        cv2.rectangle(degraded_frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
    
    # Simulate "restoration" by enhancing contrast in detected areas
    restored_frame = cv2.convertScaleAbs(degraded_frame, alpha=1.2, beta=20)
    return restored_frame

# Function to simulate sensor data (with slightly more variance)
def generate_sensor_data():
    light = random.randint(180, 220)
    temperature = round(random.uniform(20.0, 23.0), 1)
    humidity = random.randint(60, 70)
    return {
        'light': light,
        'temperature': temperature,
        'humidity': humidity
    }

# Route to display the dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route to stream video with processed frames and sensor data
@app.route('/video_feed')
def video_feed():
    # Path to the directory containing the received images
    image_directory = './'  # The directory where the received images are stored
    
    # Get all the image files in the directory (ensure they are ordered correctly)
    image_files = sorted([f for f in os.listdir(image_directory) if f.startswith('received_frame_') and f.endswith('.jpg')])
    
    def generate_frames():
        prev_sensor_data = None
        frame_count = 0
        
        for image_file in image_files:
            # Read the image from file
            frame = cv2.imread(os.path.join(image_directory, image_file))
            
            # Process the frame
            restored_frame = process_frame(frame)
            
            # Combine original and processed frames
            combined_frame = cv2.hconcat([frame, restored_frame])
            cv2.putText(combined_frame, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(combined_frame, "Restored", (frame.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Encode the frame as JPEG
            _, buffer = cv2.imencode('.jpg', combined_frame)
            frame_data = buffer.tobytes()
            
            # Generate sensor data (with slightly more variance)
            sensor_data = generate_sensor_data()
            sensor_data_json = json.dumps(sensor_data)
            
            # Yield the frame along with updated sensor data (formatted for HTML)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n'
                   b'--frame\r\n'
                   b'Content-Type: application/json\r\n\r\n' + sensor_data_json.encode() + b'\r\n\r\n')
            
            # Simulate a slight delay to mimic frame rate control (if needed)
            time.sleep(1.0 / 60.0)  # Assuming 60 FPS

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to display sensor data (example)
@app.route('/sensor_data')
def sensor_data_display():
    sensor_data = generate_sensor_data()
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

