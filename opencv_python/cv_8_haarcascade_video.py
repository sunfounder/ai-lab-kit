import cv2
from pathlib import Path

# -----------------------------
# Video + Haar cascade setup
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
video_path = str(BASE_DIR / "sample5.mp4")

# Load Haar cascade classifiers (face + eye)
face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
eye_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

# Check if cascade files are loaded correctly
if face_cascade.empty():
    raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
if eye_cascade.empty():
    raise FileNotFoundError("Failed to load haarcascade_eye.xml")

# Open video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise RuntimeError("Error opening video file")

# Get FPS from video (fallback if unavailable)
fps = cap.get(cv2.CAP_PROP_FPS)
if not fps or fps <= 1e-3:
    fps = 30.0
frame_delay_ms = int(1000 / fps)

WINDOW_NAME = "Haarcascade"

print("Playing video... press 'q' to quit")

while True:
    start_tick = cv2.getTickCount()

    ret, frame = cap.read()

    # If video ends, restart from beginning
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Convert to grayscale (Haar cascade works on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Optional: improve contrast for more stable detection
    gray = cv2.equalizeHist(gray)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(60, 60)
    )

    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

        # Detect eyes inside the face region only (faster + fewer false positives)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(
            roi_gray,
            scaleFactor=1.2,
            minNeighbors=8,
            minSize=(20, 20)
        )

        # Draw up to 2 eyes (typical for a face)
        for (ex, ey, ew, eh) in eyes[:2]:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

    # Display the result
    cv2.imshow(WINDOW_NAME, frame)

    # Compute processing time in milliseconds
    process_time_ms = (cv2.getTickCount() - start_tick) * 1000 / cv2.getTickFrequency()
    delay_ms = max(1, int(frame_delay_ms - process_time_ms))

    # Handle keyboard input and window events
    key = cv2.waitKey(delay_ms) & 0xFF
    if key == ord("q"):
        break

    # Exit if the user closes the window (click X)
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
