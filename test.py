from cv2 import VideoCapture, imshow, waitKey, destroyAllWindows, resize, cvtColor, COLOR_BGR2GRAY, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from time import time

# Define the desired resolution and fps for the regular frame
regular_frame_width = 1920  # 1080p width
regular_frame_height = 1080  # 1080p height
desired_fps = 60  # Desired frames per second

# Define the lower resolution for processing
processing_resolution = (640, 480)

# Start the timer
start_time = time()
# Open a connection to the webcam (usually 0 for the default camera)
cap = VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Error: Could not open the webcam.")
    exit()

# Set the desired resolution and fps for the regular frame
cap.set(CAP_PROP_FRAME_WIDTH, regular_frame_width)
cap.set(CAP_PROP_FRAME_HEIGHT, regular_frame_height)
cap.set(CAP_PROP_FPS, desired_fps)

# Calculate the elapsed time
elapsed_time = time() - start_time
print(f"Time taken to open the webcam: {elapsed_time:.2f} seconds")

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read a frame.")
        break

    # Resize the frame to lower resolution for processing
    ugly_frame = resize(frame, processing_resolution)

    # Convert the lower-resolution frame to grayscale
    gray_frame = cvtColor(ugly_frame, COLOR_BGR2GRAY)

    # Display the regular frame
    imshow('Regular Frame', frame)

    # Display the grayscale frame
    imshow('Grayscale Frame', gray_frame)

    # Check for the 'q' key to quit the application
    if waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
destroyAllWindows()