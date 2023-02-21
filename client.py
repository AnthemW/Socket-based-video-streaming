# 与C++交互的客户端

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



# python环境内的服务端
# import socket
# import cv2
#
# TCP_IP = '127.0.0.1'
# TCP_PORT = 4301
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)
#
# conn, addr = s.accept()
# print ('Connection address:', addr)
#
# cap = cv2.VideoCapture(0)
#
# while(True):
#     ret, frame = cap.read()
#
#     # Serialize the frame
#     data = frame.tobytes()
#     #data = pickle.dumps(frame, protocol=2)
#
#     # Send the serialized frame
#     conn.sendall(data)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
# conn.close()
# s.close()


# json格式打包的服务端
# import json
# import cv2
# import base64
# import socket
#
# TCP_IP = '127.0.0.1'
# TCP_PORT = 4301
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)
#
# conn, addr = s.accept()
# print ('Connection address:', addr)
#
# cap = cv2.VideoCapture(0)
#
# while True:
#     ret, frame = cap.read()
#
#     # Convert the frame to a base64-encoded JPEG image
#     _, buffer = cv2.imencode('.jpg', frame)
#     jpg_as_text = base64.b64encode(buffer).decode('utf-8')
#
#     # Create a dictionary containing the frame data
#     frame_dict = {
#         'width': frame.shape[1],
#         'height': frame.shape[0],
#         'data': jpg_as_text
#     }
#
#     # Serialize the dictionary to a JSON string and send it over the socket
#     data = json.dumps(frame_dict).encode('utf-8')
#     conn.sendall(data)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()
# conn.close()
# s.close()


# 与C#交互的服务端