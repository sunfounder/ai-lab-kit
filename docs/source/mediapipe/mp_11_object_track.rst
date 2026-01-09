.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_tracking:

11. Object Tracking with Pan-Tilt Camera
=============================================

In this chapter, we extend MediaPipe's object detection capabilities to create a **simple object tracking system** that automatically follows a specified object using pan-tilt servos. The system detects a target object (such as a "banana") and moves two servos to keep the object centered in the camera view.

.. image:: img/mp_object_track.png
   :alt: Object Tracking with Pan-Tilt Servos
   :align: center

**Objective:**

- Use MediaPipe Tasks for real-time object detection;
- Control pan and tilt servos based on object position;
- Implement basic proportional tracking logic;
- Provide visual feedback with OpenCV overlays.

**Approach:**

1. Initialize pan and tilt servos to center position;
2. Configure Raspberry Pi camera for video capture;
3. Load EfficientDet Lite0 model for object detection;
4. Process each frame to detect target object;
5. Calculate object position relative to frame center;
6. Move servos to center object in view;
7. Display tracking status and visual guides.

-----------------------------
1. Hardware Setup
-----------------------------



**Wiring Diagram:**

.. code-block:: none

   Servo 1 (Pan) → Channel 2 on Fusion HAT
   Servo 2 (Tilt) → Channel 3 on Fusion HAT
   Power → 5V supply (external recommended for two servos)
   Ground → Common ground

**Mechanical Assembly:**

Assemble the pan-tilt module, camera module, and servo module as shown in :ref:`assemble_fusion_hat_pan_tilt` .

- **Pan Servo (Horizontal):** Channel 2 on Fusion HAT+

   - Signal (yellow/orange) → PWM output
   - Power (red) → 5V
   - Ground (brown/black) → GND

- **Tilt Servo (Vertical):** Channel 3 on Fusion HAT+

   - Signal (yellow/orange) → PWM output
   - Power (red) → 5V
   - Ground (brown/black) → GND

----------------------------------------
2. Installation Requirements
----------------------------------------

Please make sure that:

1. You have installed OpenCV on your Raspberry Pi (see :ref:`opencv_install`);
2. You are using a display. Otherwise, please install Raspberry Pi Connect (|link_rpi_connect|) or RealVNC (:ref:`remote_desktop`) and make sure you can access the Raspberry Pi desktop through one of them;
3. You have downloaded the **ai-lab-kit** project (see :ref:`download_code`).
4. You have installed the **mediapipe** (see :ref:`mediapipe_install`).


------------------------
3. Run the Code
------------------------


Open the terminal in VNC and enter the following command:

.. code-block:: bash

   sudo python3 ~/ai-lab-kit/mediapipe/mp_tracking.py

.. note::

   Use ``sudo`` for GPIO/servo access. The script will:
   1. Initialize servos to center (0°);
   2. Start camera preview;
   3. Begin tracking "banana" by default, you can change the object to track by modifying the ``object_name`` variable in the code;
   4. Display tracking window with status.

-----------------------------
4. Code Implementation
-----------------------------

.. code-block:: python

   #!/usr/bin/env python3

   import cv2
   import time
   from fusion_hat.servo import Servo
   from picamera2 import Picamera2
   from pathlib import Path

   # MediaPipe imports
   import mediapipe as mp
   from mediapipe.tasks import python
   from mediapipe.tasks.python import vision

   # -------------------- Configuration --------------------
   TARGET = "banana"      # Object to track
   W, H = 640, 480           # Camera resolution
   CX, CY = W // 2, H // 2   # Center coordinates
   SCORE_THRESHOLD = 0.3     # Detection confidence threshold
   DEADZONE = 50             # Pixels from center before moving

   print(f"Tracking: {TARGET}")

   # -------------------- Servo Initialization --------------------
   pan = Servo(2)    # Channel 2 for pan (horizontal)
   tilt = Servo(3)   # Channel 3 for tilt (vertical)
   pan.angle(0)      # Center position
   tilt.angle(0)     # Center position
   time.sleep(1)     # Allow servos to reach position

   # -------------------- Camera Initialization --------------------
   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))
   cam.start()
   time.sleep(2)     # Allow camera to stabilize

   # -------------------- MediaPipe Detector Setup --------------------
   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")

   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

   detector = vision.ObjectDetector.create_from_options(options)

   print("Ready. Press 'q' to quit")

   # -------------------- Tracking Logic --------------------
   def simple_track(x, y):
       """Basic 4-direction tracking with deadzone"""
       if x is None:
           return 0, 0
       
       pan_move = 0
       tilt_move = 0
       
       # Left/right movement decision
       if x < CX - DEADZONE:
           pan_move = 1          # Move right
       elif x > CX + DEADZONE:
           pan_move = -1         # Move left
       
       # Up/down movement decision  
       if y < CY - DEADZONE:
           tilt_move = -1        # Move down
       elif y > CY + DEADZONE:
           tilt_move = 1         # Move up
       
       return pan_move, tilt_move

   # -------------------- Main Tracking Loop --------------------
   pan_pos = 0   # Current pan angle (-90° to +90°)
   tilt_pos = 0  # Current tilt angle (-45° to +45°)

   try:
       while True:
           # Capture frame from camera
           frame = cam.capture_array()
           frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
           
           # Convert to RGB for MediaPipe
           rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
           mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
           
           # Detect objects in frame
           detections = detector.detect_for_video(mp_image, int(time.time() * 1000))
           
           # Search for target object
           obj_x = obj_y = None
           for detection in detections.detections:
               for category in detection.categories:
                   # Case-insensitive search for target
                   if TARGET.lower() in str(category.category_name).lower():
                       bbox = detection.bounding_box
                       # Calculate object center
                       obj_x = bbox.origin_x + bbox.width // 2
                       obj_y = bbox.origin_y + bbox.height // 2
                       break
           
           # Process tracking if object found
           if obj_x is not None:
               pan_move, tilt_move = simple_track(obj_x, obj_y)
               pan_pos += pan_move
               tilt_pos += tilt_move
               
               # Limit servo angles to safe ranges
               pan_pos = max(-90, min(90, pan_pos))
               tilt_pos = max(-45, min(45, tilt_pos))
               
               # Send commands to servos
               pan.angle(pan_pos)
               tilt.angle(tilt_pos)
               
               # Draw tracking box around object
               cv2.rectangle(frame, 
                            (obj_x - 30, obj_y - 30), 
                            (obj_x + 30, obj_y + 30), 
                            (0, 255, 0), 2)
               status = f"Tracking {TARGET}"
               color = (0, 255, 0)  # Green for tracking
           else:
               status = f"No {TARGET} found"
               color = (0, 0, 255)  # Red for not found
           
           # Draw center crosshair for reference
           cv2.line(frame, (CX - 20, CY), (CX + 20, CY), (0, 255, 255), 2)
           cv2.line(frame, (CX, CY - 20), (CX, CY + 20), (0, 255, 255), 2)
           
           # Display status information
           cv2.putText(frame, status, (10, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
           cv2.putText(frame, f"Pan: {pan_pos:.0f} Tilt: {tilt_pos:.0f}", 
                      (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
           cv2.putText(frame, "Press 'q' to quit", (10, 90), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
           
           # Show video window
           cv2.imshow(f"Track: {TARGET}", frame)
           
           # Exit on 'q' key press
           if cv2.waitKey(1) & 0xFF == ord('q'):
               break

   finally:
       # -------------------- Cleanup --------------------
       pan.angle(0)      # Return to center
       tilt.angle(0)     # Return to center
       time.sleep(0.5)   # Allow movement
       cam.stop()        # Stop camera
       cv2.destroyAllWindows()  # Close display
       print("Tracking stopped. Servos centered.")

-----------------------------
5. Code Explanation
-----------------------------

**Configuration Section**

.. code-block:: python

   TARGET = "banana"
   W, H = 640, 480
   CX, CY = W // 2, H // 2
   SCORE_THRESHOLD = 0.3
   DEADZONE = 50

- ``TARGET``: Object category to track (must be in COCO dataset classes);
- ``W, H``: Camera resolution - balanced between speed and detail;
- ``CX, CY``: Frame center coordinates for tracking reference;
- ``SCORE_THRESHOLD``: Minimum confidence for valid detection;
- ``DEADZONE``: Distance from center before servo movement starts (reduces jitter).

**Servo Initialization**

.. code-block:: python

   from fusion_hat.servo import Servo
   pan = Servo(2)
   tilt = Servo(3)
   pan.angle(0)
   tilt.angle(0)

- ``Servo(2)`` and ``Servo(3)`` correspond to channels on Fusion HAT;
- ``.angle(0)`` centers servos at 0° position;
- ``time.sleep(1)`` ensures servos reach position before continuing.

**Camera Setup**

.. code-block:: python

   cam = Picamera2()
   cam.configure(cam.create_preview_configuration(
       main={"size": (W, H), "format": "XRGB8888"}
   ))

- Uses Picamera2 library for modern camera API;
- ``XRGB8888`` format provides 8-bit color channels;
- ``time.sleep(2)`` allows camera sensor to stabilize.

**MediaPipe Detector**

.. code-block:: python

   model_path = str(Path(__file__).parent / "efficientdet_lite0.tflite")
   options = vision.ObjectDetectorOptions(
       base_options=python.BaseOptions(model_asset_path=model_path),
       score_threshold=SCORE_THRESHOLD,
       running_mode=vision.RunningMode.VIDEO
   )

- Loads EfficientDet Lite0 model from same directory;
- ``RunningMode.VIDEO`` optimized for continuous frame processing;
- ``detect_for_video()`` requires timestamp for each frame.

**Tracking Function**

.. code-block:: python

   def simple_track(x, y):
       if x < CX - DEADZONE:
           pan_move = 1      # Object left → move right
       elif x > CX + DEADZONE:
           pan_move = -1     # Object right → move left
       
       if y < CY - DEADZONE:
           tilt_move = -1    # Object up → move down
       elif y > CY + DEADZONE:
           tilt_move = 1     # Object down → move up

- Simple proportional control (not true PID);
- Deadzone prevents servo jitter from small movements;
- Returns movement values of -1, 0, or 1 for each axis.

**Main Loop Processing**

.. code-block:: python

   # Object detection
   detections = detector.detect_for_video(mp_image, int(time.time() * 1000))
   
   # Find target object
   for detection in detections.detections:
       for category in detection.categories:
           if TARGET.lower() in str(category.category_name).lower():
               bbox = detection.bounding_box
               obj_x = bbox.origin_x + bbox.width // 2
               obj_y = bbox.origin_y + bbox.height // 2

1. Convert frame to MediaPipe image format;
2. Run object detection with current timestamp;
3. Search detections for target object (case-insensitive);
4. Calculate object center coordinates.

**Servo Control Logic**

.. code-block:: python

   if obj_x is not None:
       pan_move, tilt_move = simple_track(obj_x, obj_y)
       pan_pos += pan_move
       tilt_pos += tilt_move
       
       # Enforce safe angle limits
       pan_pos = max(-90, min(90, pan_pos))
       tilt_pos = max(-45, min(45, tilt_pos))
       
       pan.angle(pan_pos)
       tilt.angle(tilt_pos)

1. Get movement commands from tracking function;
2. Update position accumulators;
3. Clamp positions to mechanical limits;
4. Send new angles to servos.

**Visual Feedback**

.. code-block:: python

   # Tracking box (green when tracking)
   cv2.rectangle(frame, (obj_x-30, obj_y-30), (obj_x+30, obj_y+30), (0,255,0), 2)
   
   # Center crosshair (yellow)
   cv2.line(frame, (CX-20, CY), (CX+20, CY), (0,255,255), 2)
   cv2.line(frame, (CX, CY-20), (CX, CY+20), (0,255,255), 2)
   
   # Status text
   cv2.putText(frame, status, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

- Green box: Currently tracked object;
- Yellow crosshair: Frame center reference;
- Status text: Tracking state and servo angles.

**Cleanup Routine**

.. code-block:: python

   finally:
       pan.angle(0)
       tilt.angle(0)
       time.sleep(0.5)
       cam.stop()
       cv2.destroyAllWindows()

- Returns servos to center position;
- Stops camera capture;
- Closes OpenCV windows;
- Runs even if error occurs (``try...finally``).

------------------------------------------------------
6. Configuration Options
------------------------------------------------------

**Changing Target Object**

.. code-block:: python

   # Track different objects
   TARGET = "person"      # People tracking
   TARGET = "cup"         # Cup/glass tracking  
   TARGET = "book"        # Book tracking
   TARGET = "bottle"      # Bottle tracking

**Adjusting Tracking Parameters**

.. code-block:: python

   # Slower, smoother tracking
   DEADZONE = 75          # Larger deadzone = less sensitive
   
   # Faster, more responsive tracking  
   DEADZONE = 30          # Smaller deadzone = more sensitive
   pan_move = 2           # Larger movement steps

**Servo Range Limits**

.. code-block:: python

   # Restrict movement range
   pan_pos = max(-60, min(60, pan_pos))    # ±60° pan limit
   tilt_pos = max(-30, min(30, tilt_pos))  # ±30° tilt limit

**Performance Tuning**

.. code-block:: python

   # Lower resolution for speed
   W, H = 320, 240       # Faster processing
   
   # Higher threshold for reliability
   SCORE_THRESHOLD = 0.5  # Fewer false positives

------------------------------------------------------
7. Performance Considerations
------------------------------------------------------

.. list-table:: Performance Factors
   :header-rows: 1

   * - Factor
     - Effect on Performance
     - Recommendation
   * - Camera Resolution
     - Higher = slower detection
     - 640x480 good balance
   * - Detection Threshold
     - Lower = more detections but more false positives
     - 0.3-0.5 optimal
   * - Deadzone Size
     - Larger = smoother but less responsive
     - 40-60 pixels
   * - Servo Speed
     - Faster = more responsive but may overshoot
     - Consider acceleration control
   * - Model Size
     - Lite0 fastest, Lite2 most accurate
     - Lite0 for real-time tracking

**Expected Performance:**

- **Raspberry Pi 4:** 8-15 FPS with 640x480
- **Detection Latency:** 100-200ms
- **Servo Response Time:** 50-100ms per degree
- **Total System Latency:** 200-400ms

------------------------------------------------------
8. Troubleshooting Guide
------------------------------------------------------

.. list-table:: Common Issues and Solutions
   :header-rows: 1

   * - Issue
     - Possible Cause
     - Solution
   * - No object detection
     - Object not in COCO classes
     - Use supported object names
   * - Jerky servo movement
     - Deadzone too small
     - Increase DEADZONE to 60-80
   * - Servo overshoot
     - Movement step too large
     - Change pan_move from 1 to 0.5
   * - Low frame rate
     - Resolution too high
     - Reduce to 320x240
   * - Camera not working
     - Camera not enabled
     - Run ``sudo raspi-config``
   * - Servos not moving
     - Incorrect wiring or power
     - Check connections and power supply
   * - Object lost frequently
     - Threshold too high
     - Reduce SCORE_THRESHOLD to 0.2
   * - Incorrect tracking direction
     - Servo orientation reversed
     - Swap pan_move signs

**Debugging Tips:**

1. **Test servos separately:**
   
   .. code-block:: python

      pan.angle(45)   # Should move right
      time.sleep(1)
      pan.angle(-45)  # Should move left

2. **Verify object detection:**
   
   .. code-block:: python

      print(f"Found: {category.category_name} {c.score:.2f}")

3. **Check object coordinates:**
   
   .. code-block:: python

      print(f"Object at: ({obj_x}, {obj_y}), Center: ({CX}, {CY})")

4. **Monitor frame rate:**
   
   .. code-block:: python

      import time
      start = time.time()
      # ... processing ...
      fps = 1 / (time.time() - start)
      print(f"FPS: {fps:.1f}")

------------------------------------------------------
9. Advanced Modifications
------------------------------------------------------

**1. PID Control Implementation**

.. code-block:: python

   class PIDController:
       def __init__(self, kp=0.1, ki=0.01, kd=0.05):
           self.kp, self.ki, self.kd = kp, ki, kd
           self.prev_error = 0
           self.integral = 0
       
       def update(self, error, dt=1.0):
           self.integral += error * dt
           derivative = (error - self.prev_error) / dt
           output = self.kp*error + self.ki*self.integral + self.kd*derivative
           self.prev_error = error
           return output

**2. Multiple Object Tracking**

.. code-block:: python

   # Track closest object
   best_dist = float('inf')
   best_obj = None
   for detection in detections.detections:
       bbox = detection.bounding_box
       obj_x = bbox.origin_x + bbox.width // 2
       obj_y = bbox.origin_y + bbox.height // 2
       dist = ((obj_x - CX)**2 + (obj_y - CY)**2)**0.5
       if dist < best_dist:
           best_dist = dist
           best_obj = (obj_x, obj_y)

**3. Speed Proportional to Distance**

.. code-block:: python

   def adaptive_track(x, y):
       if x is None:
           return 0, 0
       
       # Calculate distance from center
       dx = x - CX
       dy = y - CY
       
       # Speed proportional to distance (with deadzone)
       pan_move = 0
       tilt_move = 0
       
       if abs(dx) > DEADZONE:
           pan_move = dx * 0.02  # 2% of distance per frame
           
       if abs(dy) > DEADZONE:
           tilt_move = dy * 0.02
           
       return pan_move, tilt_move

**4. Object Memory (Inertial Tracking)**

.. code-block:: python

   # Keep tracking briefly when object lost
   OBJECT_TIMEOUT = 10  # frames
   lost_counter = 0
   
   if obj_x is not None:
       last_x, last_y = obj_x, obj_y
       lost_counter = 0
   elif lost_counter < OBJECT_TIMEOUT:
       obj_x, obj_y = last_x, last_y  # Use last known position
       lost_counter += 1

------------------------------------------------------
10. Applications and Extensions
------------------------------------------------------

**Educational Applications:**

- Robotics and automation principles
- Computer vision fundamentals
- Control systems (P vs PID)
- Real-time system design

**Practical Applications:**

- Security camera auto-tracking
- Videoconferencing camera automation
- Wildlife observation
- Assistive technology for tracking

**Extension Projects:**

1. **Web Interface:** Remote control via browser
2. **Preset Positions:** Save/load common tracking positions
3. **Object Learning:** Train on custom objects
4. **Multi-camera:** Coordinate multiple tracking units
5. **Cloud Integration:** Upload tracking data for analysis
6. **Audio Feedback:** Announce tracking status
7. **Gesture Control:** Use hand gestures to control tracking

-----------------------------
11. Safety and Best Practices
-----------------------------

1. **Mechanical Safety:**

   - Secure all moving parts
   - Use cable management
   - Avoid pinch points
   - Set reasonable angle limits

2. **Electrical Safety:**

   - Use external power for servos
   - Ensure proper grounding
   - Avoid overloading power supply
   - Use appropriate gauge wires

3. **Software Safety:**

   - Always include servo centering on exit
   - Implement emergency stop mechanism
   - Log errors for debugging
   - Validate inputs and limits

4. **Operational Safety:**

   - Keep clear of moving mechanism
   - Monitor for overheating
   - Regular maintenance checks
   - Have manual override capability

-----------------------------
12. Summary
-----------------------------

This chapter demonstrated a complete object tracking system using:

1. **MediaPipe Tasks** for reliable object detection
2. **Pan-tilt servos** for physical tracking
3. **Simple proportional control** for movement logic
4. **OpenCV** for visual feedback and display

The system provides a foundation for more advanced tracking applications and demonstrates key concepts in real-time computer vision, control systems, and embedded Python programming.

By modifying the target object, adjusting parameters, and extending the control logic, this system can be adapted for various applications from educational demonstrations to practical automation solutions.

**Next Steps:**

- Implement PID control for smoother tracking
- Add object memory for temporary occlusion handling
- Create web interface for remote monitoring
- Integrate with home automation systems
- Train custom object detection models