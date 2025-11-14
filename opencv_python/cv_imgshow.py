# Python code to read image
import cv2

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# To read image from disk, we use
# cv2.imread function, in below method,
img = cv2.imread(str(BASE_DIR / "my_photo.jpg"), cv2.IMREAD_COLOR)

# Creating GUI window to display an image on screen
# first Parameter is windows title (should be in string format)
# Second Parameter is image array
cv2.imshow("Picture", img)

# To hold the window on screen, we use cv2.waitKey method
# Once it detected the close input, it will release the control
# To the next line
# First Parameter is for holding screen for specified milliseconds
# It should be positive integer. If 0 pass an parameter, then it will
# hold the screen until user close it.
cv2.waitKey(0)

# It is for removing/deleting created GUI window from screen
# and memory
cv2.destroyAllWindows()
