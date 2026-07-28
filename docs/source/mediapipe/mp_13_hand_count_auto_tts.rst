.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_hand_count_auto_tts:

13. 免接触自动 TTS — 免提语音播报
==========================================================

-----------------------------------------------------------------
1. 概述
-----------------------------------------------------------------

在 :ref:`mp_hand_count_tts`\ （第 12 节）中，我们构建了一个手势计数程序，
用户需要按下 ``t`` 键来触发 TTS 语音播报。

在本节中，我们更进一步：**完全去掉键盘。**
系统现在*自动*检测您何时保持手部姿势稳定，
并播报手指数量——无需按键，无需按钮，
完全免接触。

.. image:: img/mp_hand_count.png
   :align: center

本节课介绍了一种用于免接触交互的**状态机模式**——
这是一种可用于无障碍项目、
免提安装以及任何不方便使用键盘输入的场景的技术。

学完本课后，您将知道如何：

- 设计用于手部存在追踪的状态机
- 跨多帧检测手势*稳定性*
- 使用保持时长门控避免误触发
- 自动检测手何时进入或离开画面
- 提供多阶段视觉反馈（空闲 → 检测到 → 稳定 → 播报）
- 显示保持时长的进度条


-----------------------------------------------------------------
2. 工作原理
-----------------------------------------------------------------

程序用**基于稳定性的自动触发器**替换了键盘触发器。以下是流水线：

1. 初始化 **MediaPipe Hands** 进行实时手部检测。
2. 初始化 **Fusion HAT+ TTS 引擎**\ （Espeak）。
3. 捕获视频帧并检测手指（与之前相同）。
4. 将手指数量输入**稳定性检测器**——一个滑动窗口，
   检查连续多帧中手指数量是否保持不变。
5. 一旦确认数量稳定，启动**保持时长计时器**。
6. 如果用户保持相同姿势 2.5 秒，TTS 自动触发。
7. 如果手离开画面，系统在短暂延迟后播报"hand left the frame"。
8. **进度条**\ 和\ **多色边框**\ 一目了然地显示当前状态。

关键设计思路：

    *用户稳定的手代替了键盘——*
    系统观察*意图*（保持静止），而不是对每个短暂手势做出反应。

这使得项目完全免提和可访问——非常适合
辅助技术、互动展览或用户无法触及键盘的场景。


-----------------------------------------------------------------
3. 关键设计概念
-----------------------------------------------------------------

添加自动触发 TTS 需要比按键版本更复杂的状态管理。
让我们逐一分析每个新概念。

--------------------------------------------------
3.1 手部追踪的状态机
--------------------------------------------------

程序将手部存在追踪为一个**状态**，而不仅仅是
每帧的值。``HandTrackingState`` 类封装了
所有状态变量：

.. code-block:: python

    class HandTrackingState:
        def __init__(self):
            self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
            self.current_fingers = 0
            self.stable_fingers = -1
            self.stable_start_time = 0
            self.is_stable = False
            self.hand_present = False
            self.hand_absent_start_time = 0
            self.last_tts_time = 0
            self.last_tts_message = ""
            self.last_no_hand_tts_time = 0

    state = HandTrackingState()

通过将所有追踪变量分组到一个对象中，
即使逻辑变得更加复杂，代码也能保持有序。

状态机经过以下阶段：

- **无手** — 灰色边框，空闲状态
- **检测到手，尚未稳定** — 青色边框，"保持手部静止"提示
- **稳定，保持中** — 绿色边框填充，进度条动画
- **播报中** — 亮绿色闪烁，"SPEAKING..." 标签

--------------------------------------------------
3.2 稳定性检测
--------------------------------------------------

单帧的手指数量不可靠——由于摄像头噪声
或轻微手部移动，数字可能会闪烁。为了避免
误触发，我们使用一个**滑动窗口**来记录最近的数量：

.. code-block:: python

    from collections import deque

    FRAME_HISTORY_SIZE = 10
    STABLE_FRAMES_REQUIRED = 5

    state.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)

    def update_stability(new_count):
        state.finger_history.append(new_count)

        if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
            recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
            if all(c == new_count for c in recent_counts):
                # Gesture is stable!
                state.is_stable = True
                state.stable_start_time = time.time()
                state.current_fingers = new_count
                return True

        state.current_fingers = new_count
        return False

仅当最近 5 帧都报告相同的手指数量时，
手势才被认为是**稳定的**。这过滤了短暂的
抖动，确保系统仅在用户有意识地
保持姿势时才播报。

--------------------------------------------------
3.3 带保持时长的自动触发
--------------------------------------------------

仅有稳定性还不够——用户必须*保持*姿势
足够长的时间以表明意图：

.. code-block:: python

    HOLD_DURATION_REQUIRED = 2.5    # seconds
    MIN_TTS_INTERVAL = 4.0          # seconds between auto triggers

    def should_trigger_tts():
        now = time.time()

        # Minimum interval between TTS triggers
        if now - state.last_tts_time < MIN_TTS_INTERVAL:
            return False

        # Hand must be present and stable
        if not state.hand_present or not state.is_stable:
            return False

        # Must have been stable for the required hold duration
        hold_time = now - state.stable_start_time
        if hold_time < HOLD_DURATION_REQUIRED:
            return False

        # Don't repeat the same count too quickly
        if state.stable_fingers == state.current_fingers:
            if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
                return False

        return True

三道门控防止误触发：

1. **最小间隔** — 任意两次 TTS 事件之间至少 4 秒。
2. **保持时长** — 手势必须稳定保持 2.5 秒。
3. **重复防护** — 相同数量在 8 秒内不会再次播报。

--------------------------------------------------
3.4 手部离开检测
--------------------------------------------------

当用户将手从摄像头移开时，
系统会注意到并播报通知：

.. code-block:: python

    HAND_EXIT_DELAY = 4.0  # seconds after hand leaves

    # When hand just left:
    if state.hand_present:
        state.hand_present = False
        state.is_stable = False
        state.stable_fingers = -1
        state.finger_history.clear()

        if now - state.last_tts_time >= MIN_TTS_INTERVAL:
            tts.say("hand left the frame")

离开消息仅在距离上次 TTS 事件足够时间后
才触发——防止它打断手指数量播报。

--------------------------------------------------
3.5 构建消息
--------------------------------------------------

消息构建与按键版本相同：

.. code-block:: python

    if count == 0:
        message = "no fingers detected"
    elif count == 1:
        message = "one finger detected"
    else:
        message = f"{count} fingers detected"

.. note::

   与按键版本对双手手指求和不同，
   本版本使用 ``max(total_fingers, finger_count)`` 选择
   可见手指最多的手。当双手都在画面中时，
   这能产生更可靠的结果。

--------------------------------------------------
3.6 多阶段视觉反馈
--------------------------------------------------

与单一的绿色闪烁不同，本版本提供了
**连续的颜色编码边框**，反映当前状态：

.. code-block:: python

    COLOR_IDLE     = (128, 128, 128)   # gray   — no hand
    COLOR_DETECTED = (255, 255, 0)     # cyan   — hand seen, not yet stable
    COLOR_STABLE   = (0, 255, 0)       # green  — gesture stable, holding
    COLOR_SPEAKING = (0, 255, 0)       # bright green — TTS in progress

边框颜色随着保持时长的推进，
从青色平滑过渡到绿色，
让用户实时了解距离触发 TTS 还有多久。

**进度条**：右上角的一个小条从左向右填充，
随着保持时长增加而增长。当达到 100% 时，
TTS 触发。这给用户一个清晰的视觉倒计时。

**状态文本**：手指数量下方的状态行显示
当前阶段：

- ``"Status: No hand detected"``
- ``"Status: Detecting... keep hand still"``
- ``"Status: Hold gesture (1.3s to speak)"``
- ``"Status: Ready to speak!"``


-----------------------------------------------------------------
4. 运行代码
-----------------------------------------------------------------

.. important::

   开始之前，请确保：

   * Fusion HAT+ 已组装，扬声器已连接
   * 可以访问 Raspberry Pi 桌面
   * 代码包已安装
   * MediaPipe 和 OpenCV 已安装

   详细说明请参见 :ref:`mediapipe_install` 和 :ref:`opencv_install`。

#. 打开终端并输入以下命令：

   .. code-block:: bash

      sudo python3 ~/ai-lab-kit/mediapipe/mp_hand_count_tts_without_tap.py

#. 运行程序后：

   - 一个标题为"MediaPipe Hand Detection + AUTO TTS (Touchless Mode)"的窗口会打开，
     显示实时摄像头画面。
   - 将手举到摄像头前——手指数量会显示在
     左上角。
   - *保持手部静止* —— 观察边框从灰色
     变为青色再变为绿色，进度条逐渐填满。
   - 保持相同手势 2.5 秒后，系统
     自动播报手指数量。
   - 将手从摄像头移开——片刻之后，系统
     会播报"hand left the frame"。

   .. hint::

      试试展示不同数量的手指，每个姿势
      保持几秒钟。您应该会听到每个数量
      自动播报。注意边框颜色和
      进度条如何引导您完成整个过程。

   按 ``q`` 键退出程序。


--------------------------------------------------
5. 完整代码
--------------------------------------------------

.. code-block:: python

   """
   MediaPipe Hand Detection + Auto TTS (Touchless Mode)
   ====================================================
   Detects fingers via webcam in real time. Automatically speaks the finger count
   when a stable hand gesture is maintained for a certain duration.

   No keyboard input required for triggering TTS.

   Usage:
       python mp_hand_count_auto_tts.py

   Controls:
       'q'  - quit
   """

   from picamera2 import Picamera2
   import cv2
   import mediapipe.python.solutions.hands as mp_hands
   import mediapipe.python.solutions.drawing_utils as drawing
   import mediapipe.python.solutions.drawing_styles as drawing_styles
   from fusion_hat.tts import Espeak
   import time
   from collections import deque


   # ======================== Init TTS ========================
   tts = Espeak()
   tts.set_amp(200)       # volume 0-200, default 100
   tts.set_speed(150)     # speed 80-260, default 150
   tts.set_pitch(80)      # pitch 0-99, default 80

   # ======================== Init MediaPipe Hands ========================
   hands = mp_hands.Hands(
       static_image_mode=False,
       max_num_hands=2,
       min_detection_confidence=0.5,
       min_tracking_confidence=0.5
   )

   # ======================== Init Camera ========================
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
       main={"size": (640, 480), "format": "XRGB8888"},
   )
   picam2.configure(config)
   picam2.start()

   # ======================== Constants ========================
   # Finger tip and dip landmark indices
   FINGER_TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
   FINGER_DIPS = [2, 6, 10, 14, 18]   # corresponding middle joints

   # Auto TTS parameters
   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable before speaking
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves before saying "hand left"
   NO_HAND_COOLDOWN = 5.0          # seconds without hand before suppressing "no hand" repeats

   # Frame processing
   FRAME_HISTORY_SIZE = 10         # for stability detection

   # Border colors (BGR)
   COLOR_IDLE = (128, 128, 128)    # gray
   COLOR_DETECTED = (255, 255, 0)  # cyan
   COLOR_STABLE = (0, 255, 0)      # green
   COLOR_SPEAKING = (0, 255, 0)    # bright green

   print("=" * 60)
   print("  MediaPipe Hand Detection + AUTO TTS (Touchless Mode)")
   print("  No keyboard needed - just show a stable hand gesture")
   print("  Press 'q' to quit")
   print("=" * 60)

   # ======================== State Management ========================
   class HandTrackingState:
       def __init__(self):
           self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
           self.current_fingers = 0
           self.stable_fingers = -1
           self.stable_start_time = 0
           self.is_stable = False
           self.hand_present = False
           self.hand_absent_start_time = 0
           self.last_tts_time = 0
           self.last_tts_message = ""
           self.last_no_hand_tts_time = 0

   state = HandTrackingState()

   def get_finger_count(hand_landmarks):
       """Count fingers for a single hand (right hand logic)"""
       landmarks = hand_landmarks.landmark
       finger_count = 0

       # Thumb: extended when x_tip > x_dip (right hand)
       if landmarks[FINGER_TIPS[0]].x > landmarks[FINGER_DIPS[0]].x:
           finger_count += 1

       # Other four fingers: tip is above dip when extended (smaller y)
       for i in range(1, 5):
           if landmarks[FINGER_TIPS[i]].y < landmarks[FINGER_DIPS[i]].y:
               finger_count += 1

       return finger_count

   def update_stability(new_count):
       """Update stability state based on finger count history"""
       state.finger_history.append(new_count)

       if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
           recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
           if all(c == new_count for c in recent_counts):
               if not state.is_stable or state.current_fingers != new_count:
                   state.is_stable = True
                   state.stable_start_time = time.time()
                   state.current_fingers = new_count
                   return True
       else:
           state.is_stable = False

       state.current_fingers = new_count
       return False

   def should_trigger_tts():
       """Check if conditions are met for auto TTS"""
       now = time.time()

       if now - state.last_tts_time < MIN_TTS_INTERVAL:
           return False

       if not state.hand_present or not state.is_stable:
           return False

       hold_time = now - state.stable_start_time
       if hold_time < HOLD_DURATION_REQUIRED:
           return False

       if state.stable_fingers == state.current_fingers:
           if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
               return False

       return True

   def trigger_tts():
       """Execute TTS for current finger count"""
       now = time.time()
       count = state.current_fingers

       if count == 0:
           message = "no fingers detected"
       elif count == 1:
           message = "one finger detected"
       else:
           message = f"{count} fingers detected"

       if message == state.last_tts_message and now - state.last_tts_time < 3.0:
           return False

       print(f"[TTS] {message} (held for {HOLD_DURATION_REQUIRED}s)")
       tts.say(message)

       state.last_tts_time = now
       state.last_tts_message = message
       state.stable_fingers = count

       return True

   def trigger_hand_exit_tts():
       """Say hand has left the frame"""
       now = time.time()
       if now - state.last_tts_time >= MIN_TTS_INTERVAL:
           print("[TTS] hand left the frame")
           tts.say("hand left the frame")
           state.last_tts_time = now
           state.last_tts_message = "hand left"

   def get_border_color():
       """Determine border color based on current state"""
       now = time.time()

       if hasattr(state, 'speaking_until') and now < state.speaking_until:
           return COLOR_SPEAKING

       if not state.hand_present:
           return COLOR_IDLE

       if state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
               g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
               b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
               return (b, g, r)
           else:
               return COLOR_STABLE

       return COLOR_DETECTED

   # ======================== Main Loop ========================
   frame_count = 0
   speaking_flash_until = 0

   while True:
       # ---- 1. Capture frame ----
       frame_bgra = picam2.capture_array()
       frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       # ---- 2. Convert to RGB for MediaPipe ----
       frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       hands_detected = hands.process(frame_rgb)

       # ---- 3. Convert back to BGR for OpenCV display ----
       frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

       # ---- 4. Detect hands and count fingers ----
       total_fingers = 0
       has_hand = False

       if hands_detected.multi_hand_landmarks:
           has_hand = True
           for hand_landmarks in hands_detected.multi_hand_landmarks:
               drawing.draw_landmarks(
                   frame,
                   hand_landmarks,
                   mp_hands.HAND_CONNECTIONS,
                   drawing_styles.get_default_hand_landmarks_style(),
                   drawing_styles.get_default_hand_connections_style(),
               )

               finger_count = get_finger_count(hand_landmarks)
               total_fingers = max(total_fingers, finger_count)

       # ---- 5. Update state machine ----
       now = time.time()

       if has_hand:
           if not state.hand_present:
               state.hand_present = True
               state.is_stable = False
               state.finger_history.clear()
               print("[INFO] Hand detected")
           state.hand_absent_start_time = now
       else:
           if state.hand_present:
               state.hand_present = False
               state.is_stable = False
               state.stable_fingers = -1
               state.finger_history.clear()
               if now - state.last_tts_time >= MIN_TTS_INTERVAL:
                   trigger_hand_exit_tts()

       if has_hand:
           update_stability(total_fingers)

           if should_trigger_tts():
               if trigger_tts():
                   speaking_flash_until = now + 0.8
                   state.speaking_until = speaking_flash_until

       # ---- 6. Display information on screen ----
       display_text = f"Fingers: {total_fingers}"
       cv2.putText(frame, display_text, (10, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

       if not has_hand:
           status_text = "Status: No hand detected"
           status_color = (128, 128, 128)
       elif state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               remaining = HOLD_DURATION_REQUIRED - (now - state.stable_start_time)
               status_text = f"Status: Hold gesture ({remaining:.1f}s to speak)"
               status_color = (255, 255, 0)
           else:
               status_text = "Status: Ready to speak!"
               status_color = (0, 255, 0)
       else:
           status_text = "Status: Detecting... keep hand still"
           status_color = (0, 200, 200)

       cv2.putText(frame, status_text, (10, 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

       cv2.putText(frame, "Keep gesture still to auto-speak | 'q' to quit",
                   (10, frame.shape[0] - 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

       # ---- 7. Visual border feedback ----
       h, w = frame.shape[:2]
       thickness = 6

       if now < speaking_flash_until:
           border_color = (0, 255, 0)
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)
           cv2.putText(frame, "SPEAKING...", (w - 180, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
       else:
           border_color = get_border_color()
           cv2.rectangle(frame, (0, 0), (w - 1, h - 1), border_color, thickness)

       # ---- 8. Progress bar for hold duration ----
       if has_hand and state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           bar_width = int(w * 0.4)
           bar_height = 8
           bar_x = w - bar_width - 10
           bar_y = 10
           filled_width = int(bar_width * hold_progress)

           cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                        (60, 60, 60), -1)
           cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height),
                        (0, 255, 0), -1)

       # ---- 9. Key handling ----
       key = cv2.waitKey(1) & 0xff

       if key == ord('q'):
           break

       # ---- 10. Show frame ----
       cv2.imshow("MediaPipe Hand Detection + AUTO TTS (Touchless Mode)", frame)

   # ======================== Cleanup ========================
   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()
   print("Exited.")


--------------------------------------------------
6. 代码说明
--------------------------------------------------

让我们逐段分析代码，重点介绍
与 :ref:`mp_hand_count_tts` 中的按键版本相比新增的部分。

--------------------------------------------------
6.1 导入与新增依赖
--------------------------------------------------

.. code-block:: python

   from collections import deque
   import time

关键的补充是 ``deque``——Python ``collections`` 模块中的
双端队列。它为稳定性检测提供了固定大小的
滑动窗口：当你 ``append`` 到 ``deque(maxlen=N)`` 时，
旧项会自动丢弃，只保留最近的 N 个值。

这对于追踪最近的 5-10 个手指数量非常完美，
无需手动管理列表。

--------------------------------------------------
6.2 常量与配置
--------------------------------------------------

.. code-block:: python

   STABLE_FRAMES_REQUIRED = 5      # frames needed to confirm stability
   HOLD_DURATION_REQUIRED = 2.5    # seconds hand must stay stable
   MIN_TTS_INTERVAL = 4.0          # seconds between auto TTS triggers
   HAND_EXIT_DELAY = 4.0           # seconds after hand leaves
   NO_HAND_COOLDOWN = 5.0          # seconds before suppressing repeats
   FRAME_HISTORY_SIZE = 10         # for stability detection

   COLOR_IDLE     = (128, 128, 128)   # gray
   COLOR_DETECTED = (255, 255, 0)     # cyan
   COLOR_STABLE   = (0, 255, 0)       # green
   COLOR_SPEAKING = (0, 255, 0)       # bright green

所有计时和行为参数都在文件顶部
声明为命名常量。这使得程序易于调优——
想要更长的保持时间？更改 ``HOLD_DURATION_REQUIRED``。
想要减少播报频率？增加 ``MIN_TTS_INTERVAL``。

四种边框颜色定义了一种视觉语言：

- **灰色** — 空闲，画框中无手
- **青色** — 检测到手，但尚未稳定
- **绿色** — 手势稳定且保持中
- **亮绿色** — 正在播报

--------------------------------------------------
6.3 HandTrackingState 类
--------------------------------------------------

.. code-block:: python

   class HandTrackingState:
       def __init__(self):
           self.finger_history = deque(maxlen=FRAME_HISTORY_SIZE)
           self.current_fingers = 0
           self.stable_fingers = -1
           self.stable_start_time = 0
           self.is_stable = False
           self.hand_present = False
           self.hand_absent_start_time = 0
           self.last_tts_time = 0
           self.last_tts_message = ""
           self.last_no_hand_tts_time = 0

   state = HandTrackingState()

这个类将所有追踪变量打包到一个对象中。
每个变量都有特定的作用：

- ``finger_history`` — 最近手指数量的滑动窗口
  （由稳定性检测器使用）
- ``current_fingers`` — 当前帧的手指数量
- ``stable_fingers`` — 上次已确认稳定并被播报的数量
- ``stable_start_time`` — 当前稳定期开始的时间
- ``is_stable`` — 手势当前是否已确认稳定
- ``hand_present`` — 画框中当前是否有手
- ``hand_absent_start_time`` — 手上次离开画框的时间
- ``last_tts_time`` — 上次 TTS 事件的时间戳
- ``last_tts_message`` — 上次播报的消息（避免重复）
- ``last_no_hand_tts_time`` — 上次"无手"播报的时间戳

创建了一个全局的 ``state`` 实例，因此所有辅助函数
都可以读取和修改它，而无需传递参数。

--------------------------------------------------
6.4 稳定性检测函数
--------------------------------------------------

.. code-block:: python

   def update_stability(new_count):
       state.finger_history.append(new_count)

       if len(state.finger_history) >= STABLE_FRAMES_REQUIRED:
           recent_counts = list(state.finger_history)[-STABLE_FRAMES_REQUIRED:]
           if all(c == new_count for c in recent_counts):
               if not state.is_stable or state.current_fingers != new_count:
                   state.is_stable = True
                   state.stable_start_time = time.time()
                   state.current_fingers = new_count
                   return True
       else:
           state.is_stable = False

       state.current_fingers = new_count
       return False

这个函数是免接触系统的核心。工作原理如下：

1. **追加** 新的手指数量到滑动窗口。
2. **检查** 是否有足够的帧（至少 5 帧）。
3. **比较** 最近 5 帧——如果它们都匹配当前
   数量，则手势稳定。
4. **记录** 稳定性开始的时间（``stable_start_time``）
   ——用于保持时长计时器。
5. **返回** 首次确认稳定时的帧返回 ``True``，
   否则返回 ``False``。

``all(c == new_count for c in recent_counts)`` 表达式很优雅：
它检查窗口中*每个*值是否都匹配当前数量。
即使有一帧不同，稳定性就被打破。

--------------------------------------------------
6.5 自动 TTS 触发逻辑
--------------------------------------------------

.. code-block:: python

   def should_trigger_tts():
       now = time.time()

       if now - state.last_tts_time < MIN_TTS_INTERVAL:
           return False
       if not state.hand_present or not state.is_stable:
           return False
       hold_time = now - state.stable_start_time
       if hold_time < HOLD_DURATION_REQUIRED:
           return False
       if state.stable_fingers == state.current_fingers:
           if now - state.last_tts_time < MIN_TTS_INTERVAL * 2:
               return False
       return True

这个函数充当**门控**——所有条件必须满足
才能触发 TTS：

1. **最小间隔**：距上次 TTS 至少 4 秒。
2. **手存在且稳定**：手势必须已确认稳定。
3. **保持时长**：用户必须保持手势
   至少 2.5 秒。
4. **重复防护**：相同的手指数量在 8 秒内
   不会再次播报（2 倍最小间隔）。

.. tip::

   保持时长创建了一个清晰的*意图信号*——短暂的手势
   被忽略，但有意识的保持触发播报。
   这是与按键方法的关键区别：用户的*耐心*
   替代了按钮按下。

--------------------------------------------------
6.6 手部离开检测
--------------------------------------------------

.. code-block:: python

   # In the main loop:
   if has_hand:
       if not state.hand_present:
           # Hand just entered
           state.hand_present = True
           state.is_stable = False
           state.finger_history.clear()
           print("[INFO] Hand detected")
       state.hand_absent_start_time = now
   else:
       if state.hand_present:
           # Hand just left
           state.hand_present = False
           state.is_stable = False
           state.stable_fingers = -1
           state.finger_history.clear()
           if now - state.last_tts_time >= MIN_TTS_INTERVAL:
               trigger_hand_exit_tts()

当手进入或离开画框时，状态被重置：

- 稳定性被清除（``is_stable = False``）
- 手指历史被清空（``history.clear()``）
- 如果手刚刚离开，且距离上次 TTS 足够时间，
  系统会播报"hand left the frame"

在进入和离开时重置稳定性，可防止陈旧状态
在手部出现之间传递。

--------------------------------------------------
6.7 多色边框与进度条
--------------------------------------------------

.. code-block:: python

   def get_border_color():
       now = time.time()

       if hasattr(state, 'speaking_until') and now < state.speaking_until:
           return COLOR_SPEAKING

       if not state.hand_present:
           return COLOR_IDLE

       if state.is_stable:
           hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
           if hold_progress < 1.0:
               # Smooth blend from cyan to green
               r = int(COLOR_DETECTED[0] * (1-hold_progress) + COLOR_STABLE[0] * hold_progress)
               g = int(COLOR_DETECTED[1] * (1-hold_progress) + COLOR_STABLE[1] * hold_progress)
               b = int(COLOR_DETECTED[2] * (1-hold_progress) + COLOR_STABLE[2] * hold_progress)
               return (b, g, r)
           else:
               return COLOR_STABLE

       return COLOR_DETECTED

边框颜色不仅起装饰作用——它是实时的
状态指示器：

- **无手** → 灰色边框
- **检测到手，不稳定** → 青色边框
- **稳定，保持中** → 从青色到绿色的平滑渐变
  随着保持时长推进
- **保持完成 / 播报中** → 亮绿色边框

**进度条**\ 与边框协同工作：

.. code-block:: python

   if has_hand and state.is_stable:
       hold_progress = min(1.0, (now - state.stable_start_time) / HOLD_DURATION_REQUIRED)
       bar_width = int(w * 0.4)
       bar_height = 8
       bar_x = w - bar_width - 10
       bar_y = 10
       filled_width = int(bar_width * hold_progress)

       cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height),
                    (60, 60, 60), -1)  # background
       cv2.rectangle(frame, (bar_x, bar_y), (bar_x + filled_width, bar_y + bar_height),
                    (0, 255, 0), -1)   # fill

一个深灰色条（画框宽度的 40%）位于右上角。
随着保持时间的推进，绿色填充穿过它。
当条填满时，TTS 触发。

边框颜色和进度条共同为用户提供连续的反馈——
他们总能清楚地知道距离触发播报还有多远。


-----------------------------------------------------------------
7. 扩展思路
-----------------------------------------------------------------

免接触自动 TTS 模式开启了许多可能性：

- **辅助通信** — 将特定手势映射到
  预录短语。伸出 1 根手指表示"是"，2 根表示"否"，
  3 根表示"求助"。系统自动播报短语。

- **免提演示控制** — 保持手势以
  在演讲中推进幻灯片或触发音效。

- **互动博物馆展品** — 参观者伸出手指
  即可听到编号展品的事實信息。无需触摸。

- **GPIO 按钮集成** — 通过 ``fusion_hat`` GPIO 添加物理按钮，
  用于启用/禁用自动 TTS 模式，
  让用户手动控制系统何时监听。

- **多手势词汇表** — 扩展稳定性检测器
  以识别手势序列（例如 1 根手指 → 2 根手指
  → 3 根手指）作为触发不同动作的"命令代码"。

- **与人脸检测结合** — 当人脸进入或离开画面时
  自动播报："Person detected" / "Person left。"


-----------------------------------------------------------------
8. 故障排除
-----------------------------------------------------------------

- **TTS 触发太频繁或不稳定的手势也被触发**

  增加 ``STABLE_FRAMES_REQUIRED``\ （例如从 5 改为 8），
  以要求在确认稳定性前有更多帧的一致性。

  增加 ``HOLD_DURATION_REQUIRED``\ （例如从 2.5 改为 3.5），
  以要求在播报前保持更长时间。

- **TTS 从不触发，即使保持稳定**

  确保手部光照良好且摄像头可见。检查 ``min_detection_confidence``
  是否设置过高（0.5 是良好的默认值）。

  确认屏幕上的状态文本显示"Ready to speak!"
  ——如果一直停留在"Detecting..."或进度条从未
  填满，则稳定性检测器可能未确认。

- **"Hand left the frame"在错误时间播报**

  离开消息遵循 ``MIN_TTS_INTERVAL`` 规则——如果手指数量
  播报刚刚发生，它不会触发。如果您希望它总是播报，
  从 ``trigger_hand_exit_tts()`` 中移除 ``MIN_TTS_INTERVAL`` 检查。

- **进度条不显示**

  进度条仅在 ``has_hand`` 为 ``True`` **且** ``state.is_stable``
  为 ``True`` 时显示。如果任一条件为假，
  条就会被隐藏。检查状态文本以确定
  哪个条件失败。

- **边框颜色不变**

  验证是否每帧都调用了 ``get_border_color()``，
  并且 ``state.hand_present`` 和 ``state.is_stable``
  标志在主循环中正确更新。


-----------------------------------------------------------------
9. 总结
-----------------------------------------------------------------

- 本节课演示了如何**移除键盘触发器**
  并构建一个完全免接触的自动 TTS 系统。
- 该项目使用一个**状态机**（``HandTrackingState`` 类）
  来追踪手部存在、手势稳定性和 TTS 计时。
- **涉及的关键设计模式：**

  - **稳定性检测** — 手指数量的滑动窗口，
    以确认用户正稳定保持手势
  - **保持时长门控** — 在触发 TTS 前要求 2.5 秒的稳定性，
    用*意图*替代按键
  - **自动离开检测** — 当手消失时播报
    "hand left the frame"
  - **多阶段视觉反馈** — 颜色编码的边框
    （灰色 → 青色 → 绿色）加上实时状态进度条
  - **手部进出时状态重置** — 清除历史记录和
    稳定性，防止陈旧数据传递

- 这些模式是**项目无关的**——您可以将
  状态机 + 稳定性检测方法应用于任何需要
  免接触交互的计算机视觉项目。
- 将自动 TTS 与手势识别结合，为辅助技术、
  免提控制系统和交互式安装打开了大门。
