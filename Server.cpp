
#include <iostream>
#include <opencv2/opencv.hpp>
#include <WinSock2.h>
#include <Windows.h>

#pragma comment(lib, "Ws2_32.lib")

using namespace std;
using namespace cv;

int main(int argc, char* argv[])
{
    // Initialize Winsock
    WSADATA wsaData;
    int iResult = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (iResult != 0) {
        cout << "WSAStartup failed: " << iResult << endl;
        return 1;
    }

    // Create a socket
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (serverSocket == INVALID_SOCKET) {
        cout << "Failed to create socket: " << WSAGetLastError() << endl;
        WSACleanup();
        return 1;
    }

    // Bind the socket to a local address and port
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(4301);

    iResult = ::bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));
    if (iResult == SOCKET_ERROR) {
        cout << "Failed to bind socket: " << WSAGetLastError() << endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    // Listen for incoming connections
    iResult = listen(serverSocket, SOMAXCONN);
    if (iResult == SOCKET_ERROR) {
        cout << "Listen failed: " << WSAGetLastError() << endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    // Accept a client connection
    SOCKET clientSocket = accept(serverSocket, NULL, NULL);
    if (clientSocket == INVALID_SOCKET) {
        cout << "Accept failed: " << WSAGetLastError() << endl;
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    cout << "Client connected" << endl;

    // Initialize the video capture object
    VideoCapture cap(0);

    if (!cap.isOpened()) {
        cout << "Failed to open video capture device" << endl;
        closesocket(clientSocket);
        closesocket(serverSocket);
        WSACleanup();
        return 1;
    }

    Mat frame;

    // Start streaming video
    while (true) {
        // Capture a frame
        cap >> frame;

        if (frame.empty()) {
            cout << "Failed to capture frame" << endl;
            break;
        }

        // Serialize the frame
        vector<uchar> data;
        imencode(".jpg", frame, data);

        // Send the serialized frame
        int bytesSent = send(clientSocket, (const char*)data.data(), data.size(), 0);
        if (bytesSent == SOCKET_ERROR) {
            cout << "Failed to send data: " << WSAGetLastError();
            closesocket(clientSocket);
            closesocket(serverSocket);
            WSACleanup();
            break;
        }

        // Wait for a short period to limit the frame rate
        Sleep(100);
    }

    // Release the video capture object
    cap.release();

    // Close the sockets and cleanup Winsock
    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();

    return 0;
}

