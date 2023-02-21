# Socket-based-video-streaming
Pass video streams between C++, C#, Python environments

## Tools
VS2019，Pycharm2022，Python3.9
## Packages
OpenCV，OpencvSharp
## The project includes...
C++ server: get frames using OpenCV and send them to client  
Python client: receive frames from server and decode them  
Python server: get frames using OpenCV and send them to client  
C# client：receive frames from server, decode them, and display them in PictureBox (Use OpencvSharp to convert CvMat to Bitmap)

*These codes are just simple examples, and you can change how images are encoded and decoded to meet your specific needs*  
*Use __netstat -aon|findstr "PORT_NUMBER"__ in the Windows command prompt to confirm that the port is not occupied by another process*
