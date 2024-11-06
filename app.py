from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
import random
import json
import time

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
    # Path to the video (car driving at high speed)
    video_path = 'stock.webm'  # Updated path to your video
    video_capture = cv2.VideoCapture(video_path)
    
    # Set the desired FPS to 60
    video_capture.set(cv2.CAP_PROP_FPS, 60)
    
    # Get the actual FPS of the video
    actual_fps = video_capture.get(cv2.CAP_PROP_FPS)

    def generate_frames():
        prev_sensor_data = None
        start_time = time.time()
        frame_count = 0
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            
            # Process the frame
            restored_frame = process_frame(frame)
            
            # Combine original and processed frames
            combined_frame = cv2.hconcat([frame, restored_frame])
            cv2.putText(combined_frame, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(combined_frame, "Restored", (frame.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(combined_frame, f"FPS: {actual_fps:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
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
            
            # Maintain the desired FPS of 60
            frame_count += 1
            elapsed_time = time.time() - start_time
            if frame_count >= actual_fps:
                time_to_sleep = 1.0 / 60.0 - elapsed_time / frame_count
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
                start_time = time.time()
                frame_count = 0
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to display sensor data (example)
@app.route('/sensor_data')
def sensor_data_display():
    sensor_data = generate_sensor_data()
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
