/*
using System;
using System.Drawing;
using System.IO;
using System.Net.Sockets;
using System.Text.Json;
using System.Windows.Forms;
using System.Text;
class Program
{
    static void Main(string[] args)
    {
        // Connect to the Python server
        TcpClient client = new TcpClient("127.0.0.1", 4301);
        NetworkStream stream = client.GetStream();

        // Create a PictureBox control to display the frames
        PictureBox pictureBox = new PictureBox();
        pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
        pictureBox.Dock = DockStyle.Fill;
        Form form = new Form();
        form.Text = "Video Stream";
        form.Controls.Add(pictureBox);
        form.Show();

        // Enter a loop to receive and display the video frames
        while (true)
        {
            // Read the size of the serialized frame data
            byte[] sizeBytes = new byte[4];
            stream.Read(sizeBytes, 0, 4);
            int size = BitConverter.ToInt32(sizeBytes, 0);

            // Read the serialized frame data
            byte[] data = new byte[size];
            int bytesReceived = 0;
            while (bytesReceived < size)
            {
                bytesReceived += stream.Read(data, bytesReceived, size - bytesReceived);
            }

            // Deserialize the JSON string into a Frame object
            string json = Encoding.UTF8.GetString(data);
            Frame frame = JsonSerializer.Deserialize<Frame>(json);

            // Convert the base64-encoded JPEG image to a Bitmap
            byte[] buffer = Convert.FromBase64String(frame.Data);
            using (MemoryStream memoryStream = new MemoryStream(buffer))
            {
                Bitmap bitmap = new Bitmap(memoryStream);
                pictureBox.Image = bitmap;
            }
        }

        // Clean up resources
        stream.Close();
        client.Close();
    }

    public class Frame
    {
        public int Width { get; set; }
        public int Height { get; set; }
        public string Data { get; set; }
    }

}
*/

using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Drawing;
using System.Text;
using System.Threading.Tasks;
using OpenCvSharp;
using OpenCvSharp.Extensions;
using System.Windows.Forms;

namespace Client
{
    class Program
    {
        static void Main(string[] args)
        {
            IPAddress ip = IPAddress.Parse("127.0.0.1");
            int port = 4301;
            PictureBox pictureBox = new PictureBox();
            pictureBox.SizeMode = PictureBoxSizeMode.StretchImage;
            pictureBox.Dock = DockStyle.Fill;
            Form form = new Form();
            form.Text = "Video Stream";
            form.Controls.Add(pictureBox);
            form.Show();

            using (TcpClient client = new TcpClient())
            {
                try
                {
                    client.Connect(ip, port);

                    using (NetworkStream stream = client.GetStream())
                    using (BinaryReader reader = new BinaryReader(stream))
                    {
                        while (true)
                        {
                            // Receive the length of the incoming message as a 4-byte array
                            byte[] sizeBytes = new byte[4];
                            int bytesRead = stream.Read(sizeBytes, 0, 4);
                            if (bytesRead != 4)
                            {
                                throw new Exception("Failed to read message length");
                            }

                            // Convert the 4-byte array to an integer
                            int length = BitConverter.ToInt32(sizeBytes, 0);

                            // Receive the message itself
                            byte[] buffer = new byte[length];
                            int offset = 0;

                            while (length > 0)
                            {
                                bytesRead = stream.Read(buffer, offset, length);
                                offset += bytesRead;
                                length -= bytesRead;
                            }

                            // Decode the message into an OpenCV Mat
                            Mat image = Cv2.ImDecode(buffer, ImreadModes.Color);
                            Bitmap bmp = BitmapConverter.ToBitmap(image);
                            pictureBox.Image = bmp;

                            // Display the image
                            Cv2.ImShow("Video", image);
                            Cv2.WaitKey(1);
                        }
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ex.Message);
                }
            }
        }
    }
}


