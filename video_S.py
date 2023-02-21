# server.py

import socket
import cv2
import struct

HOST = '127.0.0.1'
PORT = 4301

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f'Server started on {HOST}:{PORT}')

while True:
    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Serialize the frame
        result, encoded_frame = cv2.imencode('.jpg', frame)

        # Get the size of the encoded frame
        size = len(encoded_frame)

        # Convert the size to a 4-byte array
        size_bytes = struct.pack('i', size)

        # Send the size to the client
        conn.sendall(size_bytes)

        # Send the encoded frame to the client
        conn.sendall(encoded_frame)

    cap.release()
    conn.close()
