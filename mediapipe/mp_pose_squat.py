from picamera2 import Picamera2, Preview
import cv2 
import mediapipe.python.solutions.pose as mp_pose
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles

# Initialize the Pose model
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    enable_segmentation=True,
)

# ---- count and threshold ----
squat_count = 0
in_bottom = False
DOWN_TH = 0.55   # Hip relative position > 0.55 is considered "full squat"
UP_TH   = 0.45   # Hip relative position < 0.45 is considered "stand up"

# Open the camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(
   main={"size": (640, 480), "format": "XRGB8888"} ,
)
picam2.configure(config)
picam2.start()

print("Streaming... press 'q' to quit")

while True:
    frame_bgra = picam2.capture_array()               # XRGB8888 to BGRA
    frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

    # Convert the frame from BGR to RGB (required by MediaPipe)
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Process the frame for pose detection and tracking
    results = pose.process(frame_rgb)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    # If pose are detected, draw landmarks and connections on the frame
    if results.pose_landmarks:
        drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
        )

        # count squat without using hip angle
        lms = results.pose_landmarks.landmark
        # left 11-23-27 (shoulder, hip, ankle)
        # right 12-24-28 (shoulder, hip, ankle)
        idx_sets = [(11,23,27), (12,24,28)]
        hip_rel_list = []

        for sh, hp, an in idx_sets:
            try:
                y_sh, y_hp, y_an = lms[sh].y, lms[hp].y, lms[an].y
                base = abs(y_an - y_sh)  # distance between shoulder and ankle
                if base > 1e-6:
                    hip_rel = (y_hp - y_sh) / base  # position of hip relative to shoulder , 0.5 means hip is in the middle , 0 means hip is at the top, 1 means hip is at the bottom
                    hip_rel_list.append(hip_rel)
            except IndexError:
                pass

        if hip_rel_list:
            hip_rel = min(hip_rel_list)  # choose the smaller one, which is more stable
            # state machine: 
            # from low -> mark "in_bottom"; 
            # from back to high -> count +1
            if not in_bottom and hip_rel >= DOWN_TH:
                in_bottom = True
            elif in_bottom and hip_rel <= UP_TH:
                squat_count += 1
                in_bottom = False

            # display
            cv2.putText(frame, f"Squats: {squat_count}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.putText(frame, f"HipRel: {hip_rel:.2f}", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
