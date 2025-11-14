from picamera2 import Picamera2, Preview
import cv2 
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles

# Initialize the Hands model
hands = mp_hands.Hands(
    static_image_mode=False,  # Set to False for processing video frames
    max_num_hands=2,           # Maximum number of hands to detect
    min_detection_confidence=0.5  # Minimum confidence threshold for hand detection
)

# Open the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
   main={"size": (640, 480), "format": "XRGB8888"} ,
)

picam2.configure(config)
picam2.start()

print("Streaming... press 'q' to quit")

# finger tips and dips
finger_tips = [4, 8, 12, 16, 20]
finger_dips = [2, 6, 10, 14, 18]


while True:
    frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
    frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert the frame from BGR to RGB (required by MediaPipe)
    frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Process the frame for hand detection and tracking
    hands_detected = hands.process(frame)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # If hands are detected, draw landmarks and connections on the frame
    if hands_detected.multi_hand_landmarks:
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )


            # Count the number of fingers raised (right hand)
            landmarks = hand_landmarks.landmark
            finger_count = 0

            # check if thumb is up
            if landmarks[finger_tips[0]].x > landmarks[finger_dips[0]].x:
                finger_count += 1

            # check if the other fingers are up
            for i in range(1, 5):
                if landmarks[finger_tips[i]].y < landmarks[finger_dips[i]].y:
                    finger_count += 1

            # Display the number of fingers raised
            cv2.putText(frame, f"Fingers: {finger_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
