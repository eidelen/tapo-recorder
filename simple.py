# resources: https://github.com/xelest/tapo_c200_python_opencv

import argparse
import cv2    # pip install opencv-python

parser = argparse.ArgumentParser(description='Record images when motion')
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('ip')

args = parser.parse_args()

user = args.user # user you set in Advanced Settings -> Camera Account
password = args.password # password you set in Advanced Settings -> Camera Account
host = args.ip # ip of the camera, example: 192.168.1.52
port = 554

url_1080p = f"rtsp://{user}:{password}@{host}:{port}/stream1"

print(url_1080p)

cap = cv2.VideoCapture(url_1080p)

if not cap.isOpened():
    print("Failed to open RTSP stream")
    exit()

while True:
    # Read a frame from the RTSP stream
    ret, frame = cap.read()

    # Check if the frame is read correctly
    if not ret:
        print("Failed to read frame")
        break

    # Display the frame
    cv2.imshow("RTSP Stream", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the RTSP stream and close the window
cap.release()
cv2.destroyAllWindows()


