import cv2 
import mediapipe.python.solutions.pose as mp_pose
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles

# Initialize the Pose model
pose = mp_pose.Pose(
    static_image_mode=False,  # Set to False for processing video frames
    model_complexity=1,
    enable_segmentation=True,
)

# Get path of the video
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / 'sample9.mp4')

# read video
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print('Error opening video file')
    exit()


while True:
    start_time = cv2.getTickCount()
    ret, frame = cap.read()

    # If video ends, restart from beginning
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Convert the frame from BGR to RGB (required by MediaPipe)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame for pose detection and tracking
    results = pose.process(frame)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # If pose are detected, draw landmarks and connections on the frame
    if results.pose_landmarks:
        drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
        )

    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Calculate delay to maintain desired FPS
    expected_delay = max(1, int(1000 / cap.get(cv2.CAP_PROP_FPS)))
    process_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
    delay = int(expected_delay - process_time)
    
    # Ensure delay is non-negative
    delay = max(0, delay)
    


    # Wait for the next frame
    k = cv2.waitKey(delay) & 0xff
    if k == ord('q'):
        break

# Release video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
