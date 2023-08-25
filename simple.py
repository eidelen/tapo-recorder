# resources: https://github.com/xelest/tapo_c200_python_opencv

import argparse
import numpy as np
from datetime import datetime
from itertools import product

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

url_1080p = f"rtsp://{user}:{password}@{host}:{port}/stream2"

print(url_1080p)

cap = cv2.VideoCapture(url_1080p)

if not cap.isOpened():
    print("Failed to open RTSP stream")
    exit()

prev_fame = None
is_recording = False
length_recording = 80
k_recording = 0
video_writer = None


while True:
    # Read a frame from the RTSP stream and convert to grayscale
    ret, frame = cap.read()
    h, w, c = frame.shape
    frame_gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if c == 3 else frame

    # Check if the frame is read correctly
    if not ret:
        print("Failed to read frame")
        break

    if is_recording:
        k_recording += 1
        cv2.imshow("RTSP Stream", frame_gs)
        video_writer.write(frame_gs)
        if k_recording > length_recording:
            is_recording = False
            prev_fame = None
            video_writer.release()
            print("Stop recording")


    else:
        # check if there is motion
        if prev_fame is not None:
            diff_img = cv2.subtract(frame_gs, prev_fame)
            err = np.sum(diff_img ** 2)
            mse = err / (float(h * w))


            # record a movie if there is motion
            if mse > 2.5:
                is_recording = True
                k_recording = 0
                recording_file_name = f"recs/{datetime.now():%Y-%m-%d_%H-%M-%S}.avi"
                video_writer = cv2.VideoWriter(recording_file_name, cv2.VideoWriter_fourcc(*'MJPG'), 10, (w, h),
                                               isColor=False)
                print("Start recording: ", mse)
                #cv2.imshow("RTSP Stream", frame_gs)

        prev_fame = frame_gs

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the RTSP stream and close the window
cap.release()
cv2.destroyAllWindows()


