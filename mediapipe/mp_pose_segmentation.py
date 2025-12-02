from picamera2 import Picamera2, Preview
import cv2 
import mediapipe.python.solutions.pose as mp_pose
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles

import numpy as np
GREEN = (0, 255, 0)  # green color（BGR）

# Initialize the Pose model
pose = mp_pose.Pose(
    static_image_mode=False,  # Set to False for processing video frames
    model_complexity=1,
    enable_segmentation=True,
)

# Open the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
   main={"size": (640, 480), "format": "XRGB8888"} ,
)

picam2.configure(config)
#picam2.start_preview(Preview.QTGL) 
picam2.start()

print("Streaming... press 'q' to quit")


# --- Utility: empty callback for trackbars ---
def _noop(x):
    pass

# create Window
cv2.namedWindow('Show Video')
# create a trackbar for threshold ,default value is 50
cv2.createTrackbar('Mask', 'Show Video', 50, 100, _noop)


while True:
    frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
    frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert the frame from BGR to RGB (required by MediaPipe)
    frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Process the frame for pose detection and tracking
    results = pose.process(frame)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # read the trackbar value
    threshold = cv2.getTrackbarPos('Mask', 'Show Video')

    # cutout the green background
    if results.segmentation_mask is not None:
        # segmentation_mask is a single-channel [H, W] probability map.
        mask = results.segmentation_mask
        # Use 0.5 as the hard threshold; you can adjust it to 0.3-0.7 based on the effect.
        condition = (mask > threshold/100.0)[..., None]  # [H, W, 1]

        # create a green background
        bg = np.full_like(frame, GREEN, dtype=np.uint8)

        # Use mask to keep the character and replace the background with green
        frame = np.where(condition, frame, bg)

    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
