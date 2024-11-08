# Neutron
![Team](https://github.com/user-attachments/assets/2c0193e3-3796-40c9-a32b-f0dc588d9f01)
## Overview
This project uses Detectron2 and Flask to serve a dashboard that streams a processed video feed along with simulated sensor data. It employs a Faster R-CNN model to detect objects in each frame of a video, highlights them with bounding boxes, and applies a simple "restoration" effect on the detected areas. The app runs a real-time dashboard that displays both the original and processed video frames along with simulated sensor readings for light, temperature, and humidity.

## Model Specifications
- **Model Type**: Faster R-CNN (Region-based Convolutional Neural Network)
- **Base Architecture**: ResNet-50 with Feature Pyramid Network (FPN)
- **Framework**: Detectron2 (built on PyTorch)
- **Dataset**: Pre-trained on COCO Dataset (common objects in context)
- **Configuration**: `faster_rcnn_R_50_FPN_3x.yaml`
- **Confidence Threshold**: 0.5
- **Device**: CPU (configurable to GPU if available)

## Features
![image](https://github.com/user-attachments/assets/63308b27-5754-4801-be14-4001fbb193bd)
- **Object Detection**: Uses Faster R-CNN to detect objects in the video feed.
- **Frame Processing**: Frames are processed to include bounding boxes and enhanced contrast for detected areas.
- **Sensor Data Simulation**: Light, temperature, and humidity data are simulated and displayed alongside the video stream.
- **Dashboard Interface**: Displays the original and restored video frames, annotated with real-time sensor data.

## Setup and Installation

### Prerequisites
- Python 3.7 or higher
- [Detectron2](https://github.com/facebookresearch/detectron2) and OpenCV libraries

### Install dependencies
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone git@github.com:spirizeon/neutron-hacks
   cd neutron-hacks
   ```
2. Set up a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Install Detectron2
For Detectron2, follow the [official installation instructions](https://detectron2.readthedocs.io/en/latest/tutorials/install.html), or use the following commands:
   ```bash
   python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
   ```

### Usage
1. **Place the Video**: Ensure that a video file (e.g., `stock.webm`) is in the same directory as the script or update the path in the `video_feed` route if needed.
2. **Run the Application**:
   ```bash
   python app.py
   ```
3. **Access the Dashboard**: Open a browser and go to `http://127.0.0.1:5000/` to view the real-time dashboard.

## Code Overview
- `initialize_frcnn_model()`: Initializes the Faster R-CNN model with a COCO-trained configuration.
- `process_frame(frame)`: Processes each video frame, applies bounding boxes and contrast enhancement on detected objects.
- `generate_sensor_data()`: Simulates sensor data for light, temperature, and humidity readings.
- **Routes**:
  - `/`: Renders the dashboard page.
  - `/video_feed`: Streams the processed video feed with the original and restored frames.
  - `/sensor_data`: Returns simulated sensor data in JSON format.

## Notes
- Ensure that your video file path is correct.
- For faster processing, use a GPU-enabled environment if available by setting `cfg.MODEL.DEVICE` to `"cuda"`.








