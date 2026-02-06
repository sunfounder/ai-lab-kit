# Python code to read and display an image using OpenCV
import cv2
from pathlib import Path

# Get the directory of the current Python file
BASE_DIR = Path(__file__).resolve().parent

# Read image from disk
# cv2.imread loads the image as a NumPy array
img = cv2.imread(str(BASE_DIR / "my_photo.jpg"), cv2.IMREAD_COLOR)

# Create a GUI window to display the image
# First parameter: window title
# Second parameter: image array
cv2.imshow("Picture", img)

# Keep the window open until the user closes it or presses 'q'
# cv2.waitKey only listens for keyboard events, not the close button
# Therefore, we use a loop to detect both window close and key press
while True:
    # Check if the window has been closed
    if cv2.getWindowProperty("Picture", cv2.WND_PROP_VISIBLE) < 1:
        break

    # Wait for 1 ms and check for key press
    # Press 'q' to exit the program
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Destroy all OpenCV windows and release memory
cv2.destroyAllWindows()
