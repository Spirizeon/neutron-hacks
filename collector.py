import socket
import pickle
import struct
import cv2

# Set up client to connect to the Raspberry Pi server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.86.243"  # Replace with the Pi's actual IP
port = 5000

try:
    client_socket.connect((host_ip, port))
    print("Connected to server.")
except ConnectionError:
    print("Failed to connect to the server.")
    client_socket.close()
    exit()

data = b""
payload_size = struct.calcsize("Q")

try:
    frame_count = 0  # To save frames with unique names
    while True:
        # Retrieve message size
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)
            if not packet:
                break
            data += packet

        if len(data) < payload_size:
            print("Connection closed by server.")
            break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Retrieve the frame data
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the frame
        frame = pickle.loads(frame_data)
        
        # Save frame to disk
        frame_filename = f"received_frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)
        print(f"Saved frame {frame_count} as {frame_filename}")
        
        frame_count += 1

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    print("Client connection closed.")
import socket
import pickle
import struct
import cv2

# Set up client to connect to the Raspberry Pi server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = "192.168.86.243"  # Replace with the Pi's actual IP
port = 5000

try:
    client_socket.connect((host_ip, port))
    print("Connected to server.")
except ConnectionError:
    print("Failed to connect to the server.")
    client_socket.close()
    exit()

data = b""
payload_size = struct.calcsize("Q")

try:
    frame_count = 0  # To save frames with unique names
    while True:
        # Retrieve message size
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)
            if not packet:
                break
            data += packet

        if len(data) < payload_size:
            print("Connection closed by server.")
            break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        # Retrieve the frame data
        while len(data) < msg_size:
            data += client_socket.recv(4 * 1024)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        # Deserialize the frame
        frame = pickle.loads(frame_data)
        
        # Save frame to disk
        frame_filename = f"received_frame_{frame_count}.jpg"
        cv2.imwrite(frame_filename, frame)
        print(f"Saved frame {frame_count} as {frame_filename}")
        
        frame_count += 1

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client_socket.close()
    print("Client connection closed.")

