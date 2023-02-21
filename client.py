import cv2
import socket
import numpy as np

# Initialize socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 4301))  # Connect to server

# Receive and decode frames
data = b''
while True:
    # Receive data from the server
    packet = client_socket.recv(65536)
    if not packet:
        break
    data += packet

    # Decode the received data into a frame
    while True:
        start_idx = data.find(b'\xff\xd8')
        end_idx = data.find(b'\xff\xd9', start_idx)
        if start_idx != -1 and end_idx != -1:
            frame_data = data[start_idx:end_idx+2]
            data = data[end_idx+2:]
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break

# Cleanup
client_socket.close()
cv2.destroyAllWindows()
