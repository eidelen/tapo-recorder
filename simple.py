# resources: https://github.com/xelest/tapo_c200_python_opencv

import argparse
from datetime import datetime
import collections
import cv2    # pip install opencv-python

import img_proc as ip

parser = argparse.ArgumentParser(description='Record images when motion')
parser.add_argument('user')
parser.add_argument('password')
parser.add_argument('ip')

args = parser.parse_args()

user = args.user # user you set in Advanced Settings -> Camera Account
password = args.password # password you set in Advanced Settings -> Camera Account
host = args.ip # ip of the camera, example: 192.168.1.52
port = 554
length_recording = 80 # frames
length_prev_recording_buffer = 20 # frames


url_1080p = f"rtsp://{user}:{password}@{host}:{port}/stream2" # stream1 -> higher resolution
print(url_1080p)

cap = cv2.VideoCapture(url_1080p)

if not cap.isOpened():
    print("Failed to open RTSP stream")
    exit()

prev_frame = None
is_recording = False

k_recording = 0
video_writer = None
frame_ring_buffer = collections.deque(maxlen=length_prev_recording_buffer)

while True:
    # Read a frame from the RTSP stream and convert to grayscale
    ret, frame = cap.read()
    h, w, c = frame.shape
    frame_gs = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if c == 3 else frame

    frame_ring_buffer.append(frame_gs)

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
            prev_frame = None
            video_writer.release()
            print("Stop recording")

    else:
        # check if there is motion
        if prev_frame is not None:
            mse = ip.mean_square_error(frame_gs, prev_frame)

            # record a movie if there is motion
            if mse > 80.0:
                is_recording = True
                k_recording = 0

                # create new recording and add the whole frame buffer
                recording_file_name = f"recs/{datetime.now():%Y-%m-%d_%H-%M-%S}-MSE={mse}.avi"
                video_writer = cv2.VideoWriter(recording_file_name, cv2.VideoWriter_fourcc(*'MJPG'), 10, (w, h),
                                               isColor=False)
                while frame_ring_buffer:
                    video_writer.write(frame_ring_buffer.popleft())

                print("Start recording: MSE=", mse)

        prev_frame = frame_gs

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the RTSP stream and close the window
cap.release()
cv2.destroyAllWindows()


