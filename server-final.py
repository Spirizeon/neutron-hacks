import cv2
import socket
import struct
import pickle
import subprocess
import signal
import sys
import threading

# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '0.0.0.0'  # Listen on all available interfaces
port = 5000
server_socket.bind((host_ip, port))
server_socket.listen(5)
print("Server listening on:", (host_ip, port))

# Gracefully handle shutdown
def shutdown_server(signal, frame):
    print("\nShutting down server...")
    server_socket.close()
    sys.exit(0)

# Register signal handlers for clean shutdown on CTRL+C
signal.signal(signal.SIGINT, shutdown_server)
signal.signal(signal.SIGTERM, shutdown_server)

def start_yolov5_detection():
    """ Start YOLOv5 detection using subprocess """
    print("Starting YOLOv5 detection using detect.py...")
    try:
        # Command for running YOLOv5 detection with webcam
        command = [
            "python3", "detect.py", "--source", "0", "--weights", "yolov5s.pt", "--img", "640", "--conf", "0.25"
        ]
        # Start detection process
        detection_process = subprocess.Popen(command)
        return detection_process
    except Exception as e:
        print(f"Error starting YOLOv5 detection: {e}")
        return None

def handle_client(client_socket):
    """ Handle communication with the connected client """
    print('Client connected:', client_socket.getpeername())
    
    # Start YOLOv5 detection process for the client
    detection_process = start_yolov5_detection()
    
    if detection_process is None:
        client_socket.close()
        return
    
    # Start video capture
    vid = cv2.VideoCapture(0)
    try:
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret:
                break

            # Serialize the frame
            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data
            
            # Send the data to the client
            try:
                client_socket.sendall(message)
            except (BrokenPipeError, ConnectionResetError):
                print("Client disconnected.")
                break

    finally:
        vid.release()
        client_socket.close()
        detection_process.terminate()  # Stop YOLOv5 detection when the client disconnects
        print("YOLOv5 detection stopped.")

def main():
    """ Main server loop that accepts client connections """
    try:
        while True:
            client_socket, addr = server_socket.accept()
            print('Connection from:', addr)

            # Handle each client connection in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

    finally:
        # Ensure the server socket is closed upon exiting the program
        print("Closing server socket...")
        server_socket.close()
        print("Server socket closed.")

if __name__ == "__main__":
    main()

