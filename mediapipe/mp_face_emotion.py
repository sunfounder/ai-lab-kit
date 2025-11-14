from picamera2 import Picamera2, Preview
import cv2 
import mediapipe.python.solutions.face_mesh as mp_face_mesh
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import numpy as np


# --------- Emotion judgment auxiliary function ---------
def euclidean(p1, p2):
    return np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))

def classify_emotion(landmarks):
    """
    landmarks: results.multi_face_landmarks[0].landmark (length ~468)
    Returns (label, details_dict) for easy parameter adjustment and viewing
    """
    # Keypoint Index (MediaPipe 468 points)
    L_EYE_TOP, L_EYE_BOT = 159, 145
    R_EYE_TOP, R_EYE_BOT = 386, 374
    L_EYE_CENTER, R_EYE_CENTER = 33, 263
    MOUTH_LEFT, MOUTH_RIGHT = 61, 291
    LIP_UP, LIP_DOWN = 13, 14

    # Scale normalization: distance between the centers of the two eyes
    io = euclidean(landmarks[L_EYE_CENTER], landmarks[R_EYE_CENTER])
    if io < 1e-6:
        return "Neutral", {}

    mouth_width = euclidean(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT]) / io
    mouth_open  = euclidean(landmarks[LIP_UP], landmarks[LIP_DOWN]) / io
    eye_open_L  = euclidean(landmarks[L_EYE_TOP], landmarks[L_EYE_BOT]) / io
    eye_open_R  = euclidean(landmarks[R_EYE_TOP], landmarks[R_EYE_BOT]) / io
    eye_open    = 0.5 * (eye_open_L + eye_open_R)

    # ------- Simple Rules (Thresholds can be fine-tuned per asset) -------
    # These thresholds are common at 640x480 and normal viewing distance; can be fine-tuned based on distance from the camera.
    # Priority: Surprised > Happy > Sad > Angry > Neutral
    if mouth_open > 0.08 and eye_open > 0.055:
        label = "Surprised"
    elif mouth_width > 0.48 and mouth_open > 0.035:
        label = "Happy"
    elif mouth_open < 0.018 and mouth_width < 0.36 and eye_open < 0.03:
        label = "Sad"
    elif mouth_open < 0.02 and eye_open < 0.028:
        label = "Angry"
    else:
        label = "Neutral"

    details = {
        "mouth_width": round(mouth_width, 3),
        "mouth_open": round(mouth_open, 3),
        "eye_open": round(eye_open, 3),
    }
    return label, details

# initialize the mp_face_mesh model
face = mp_face_mesh.FaceMesh(
    static_image_mode=False,  # Set to False for processing video frames
    max_num_faces=1,           # Maximum number of faces to detect
    refine_landmarks=True,  # Enable landmark refinement
    min_detection_confidence=0.5  # Minimum confidence threshold for face detection
)


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
    frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    # Process the frame for face detection and tracking
    results = face.process(frame)

    # Convert the frame back from RGB to BGR (required by OpenCV)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # If face are detected, draw landmarks and connections on the frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # --------- detect the emotion ---------
            label, metrics = classify_emotion(face_landmarks.landmark)

            # disyplay the emotion label on the frame
            cv2.putText(frame, f"Emotion: {label}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

            # if you need to debug, you can display the metrics
            dbg = f"mw:{metrics.get('mouth_width',0)} mo:{metrics.get('mouth_open',0)} eo:{metrics.get('eye_open',0)}"
            cv2.putText(frame, dbg, (20, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)


    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
 



