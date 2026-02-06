# Face and eye detection using Raspberry Pi Camera (Picamera2 + OpenCV Haar Cascades)
import cv2
from picamera2 import Picamera2
from pathlib import Path

# -----------------------------
# Load Haar cascade classifiers
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent

face_cascade = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_frontalface_default.xml"))
eye_cascade  = cv2.CascadeClassifier(str(BASE_DIR / "haarcascade_eye.xml"))

# Check if cascade files are loaded correctly
if face_cascade.empty():
    raise FileNotFoundError("Failed to load haarcascade_frontalface_default.xml")
if eye_cascade.empty():
    raise FileNotFoundError("Failed to load haarcascade_eye.xml")

# -----------------------------
# Initialize Picamera2
# -----------------------------
picam2 = Picamera2()

# Video configuration (resolution can be adjusted)
config = picam2.create_video_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

WIN = "Raspberry Pi Camera - Face Detection"
print("Camera started. Press 'q' to quit.")

try:
    while True:
        # Capture a frame (Picamera2 typically provides RGB)
        frame_rgb = picam2.capture_array()

        # Convert RGB -> Grayscale directly (faster than RGB->BGR->GRAY)
        gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)

        # Improve contrast to make detection more stable under different lighting
        gray = cv2.equalizeHist(gray)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(60, 60)
        )

        # Convert RGB -> BGR only for display and drawing (OpenCV imshow expects BGR)
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Draw face and eye results
        for i, (x, y, w, h) in enumerate(faces, start=1):
            # Draw face rectangle + label
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (255, 255, 0), 2)
            cv2.putText(frame_bgr, f"Face {i}", (x, max(0, y - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            # ROI for eye detection (search eyes only inside the detected face area)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame_bgr[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(
                roi_gray,
                scaleFactor=1.2,
                minNeighbors=8,
                minSize=(20, 20)
            )

            # Draw up to 2 eyes (typical for a face)
            for (ex, ey, ew, eh) in eyes[:2]:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 127, 255), 2)

        # Show the frame
        cv2.imshow(WIN, frame_bgr)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # Exit if the user closes the window (click X)
        if cv2.getWindowProperty(WIN, cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Camera stopped.")
