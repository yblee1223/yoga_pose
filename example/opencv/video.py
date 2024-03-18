import cv2

# Define your GStreamer pipeline
# Example pipeline to capture video from a webcam:
# pipeline = 'v4l2src device=/dev/video0 ! videoconvert ! appsink'

# Example pipeline to play a video file:
pipeline = 'filesrc location=/home/whatslab/Repository/yoga_pose/data/dance/solo.mp4 ! decodebin ! videoconvert ! appsink'

# Create VideoCapture object with GStreamer pipeline
cap = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Error: Unable to open GStreamer pipeline")
    exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read frame")
        break

    # Display the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
