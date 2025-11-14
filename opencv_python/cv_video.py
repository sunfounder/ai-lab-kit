import cv2

# Get path of the video
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / 'sample2.mp4')

# Read video
cap = cv2.VideoCapture(video_path)

while True:
    start_time = cv2.getTickCount()
    ret, frame = cap.read()
    
    # If video ends, restart from beginning
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Resize frame for better display
    frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
    
    # Show results
    cv2.imshow('Video', frame)

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

# Destroy all opened windows
cv2.destroyAllWindows()
