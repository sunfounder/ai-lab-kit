import cv2

# Open the video file
cap = cv2.VideoCapture("sample2.mp4")

while True:
    # Read one frame from the video
    ret, frame = cap.read()

    # If the video ends, restart from the beginning
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Resize the frame for better display performance
    frame = cv2.resize(frame, (640, 480))

    # Display the frame in a window named "Video"
    cv2.imshow("Video", frame)

    # Wait 30 ms between frames (~30 FPS)
    # This also processes GUI events (keyboard and window events)
    key = cv2.waitKey(30) & 0xFF

    # Press 'q' to exit the program
    if key == ord("q"):
        break

    # Exit if the user closes the window (click the close button)
    if cv2.getWindowProperty("Video", cv2.WND_PROP_VISIBLE) < 1:
        break

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
