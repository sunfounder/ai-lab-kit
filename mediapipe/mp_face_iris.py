from picamera2 import Picamera2, Preview
import cv2 
import mediapipe.python.solutions.face_mesh as mp_face_mesh
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles


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
#picam2.start_preview(Preview.QTGL) 
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
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_styles.get_default_face_mesh_contours_style()
            )
            drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_styles.get_default_face_mesh_iris_connections_style()
            )



    # Display the frame with annotations
    cv2.imshow("Show Video", frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

# Release the camera
picam2.stop_preview()
picam2.stop()
cv2.destroyAllWindows()
 