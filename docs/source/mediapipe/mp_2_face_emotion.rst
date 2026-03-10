.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _mp_face_emotion:

2. 表情認識（Emotion Detection）
==========================================

-----------------------------
1. 概要
-----------------------------

このセクションでは、Face Mesh の検出機能を拡張し、  
基本的な表情認識を行います。

ディープラーニングモデルを使用する代わりに、  
顔ランドマークの幾何情報（目と口の比率）を利用して  
リアルタイムで表情を分類します。

.. image:: img/mp_face_emotion_happy.png
   :align: center

認識できる表情：

- 😮 Surprised（驚き）
- 😀 Happy（喜び）
- 😢 Sad（悲しみ）
- 😠 Angry（怒り）
- 😐 Neutral（無表情）

-----------------------------
2. 動作原理
-----------------------------

プログラムは次の手順で動作します：

1. ``Picamera2`` + ``MediaPipe FaceMesh`` を使用して 468 個のランドマークを取得  
2. 目と口の周囲にある重要な特徴点を選択  
3. 正規化された比率を計算  

   - 目の開き具合  
   - 口の横幅  
   - 口の開き具合  

4. 設定済みの閾値と比較  
5. OpenCV を使用して検出された表情を表示  

この方法の利点：

- 高速で軽量（Raspberry Pi に適している）  
- ニューラルネットワークが不要  
- 閾値を簡単に調整できる  

------------------------
3. コードの実行
------------------------

.. important::

   開始する前に、以下を確認してください：

   * パンチルト機構が組み立てられている  
   * Raspberry Pi のデスクトップにアクセスできる  
   * コードパッケージがインストールされている  
   * Fusion HAT+ がインストールおよび設定されている  
   * OpenCV がインストールされている  


   詳細な手順は :ref:`opencv_install` を参照してください。

#. ターミナルを開き、次のコマンドを入力します：

   .. code-block:: bash

        sudo python3 ~/ai-lab-kit/mediapipe/mp_face_emotion.py

#. プログラムを実行すると、ビデオウィンドウが開き、カメラのライブ映像が表示されます。

   .. raw:: html
   
         <video width="500" loop muted controls>
             <source src="../_static/video/Media_2.mp4" type="video/mp4">
             Your browser does not support the video tag.
         </video>

   カメラの前に顔が現れると、システムは次の処理を行います：

   - 468 個の顔ランドマークをリアルタイムで検出  
   - 目の開き具合と口の開き具合の比率を計算  
   - 現在の表情を分類  

   検出された表情ラベル（ ``Happy`` 、 ``Surprised`` 、 ``Sad`` 、 ``Angry`` 、 ``Neutral`` など）が動画画面上に表示されます。

   ユーザーの表情が変化すると、表情ラベルもリアルタイムで更新されます。

   顔が検出されない場合は、通常のカメラ映像のみが表示され、表情ラベルは表示されません。

   ``q`` を押すとプログラムを終了できます。カメラは停止し、OpenCV ウィンドウは自動的に閉じます。


-----------------------------
4. 完全なコード
-----------------------------

.. code-block:: python

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
       Returns (label, details_dict)
       """
       # Keypoint Index (MediaPipe 468 points)
       L_EYE_TOP, L_EYE_BOT = 159, 145
       R_EYE_TOP, R_EYE_BOT = 386, 374
       L_EYE_CENTER, R_EYE_CENTER = 33, 263
       MOUTH_LEFT, MOUTH_RIGHT = 61, 291
       LIP_UP, LIP_DOWN = 13, 14

       # Normalization scale: distance between left and right eye centers
       io = euclidean(landmarks[L_EYE_CENTER], landmarks[R_EYE_CENTER])
       if io < 1e-6:
           return "Neutral", {}

       mouth_width = euclidean(landmarks[MOUTH_LEFT], landmarks[MOUTH_RIGHT]) / io
       mouth_open  = euclidean(landmarks[LIP_UP], landmarks[LIP_DOWN]) / io
       eye_open_L  = euclidean(landmarks[L_EYE_TOP], landmarks[L_EYE_BOT]) / io
       eye_open_R  = euclidean(landmarks[R_EYE_TOP], landmarks[R_EYE_BOT]) / io
       eye_open    = 0.5 * (eye_open_L + eye_open_R)

       # --------- Simple threshold rules (adjustable) ---------
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

   # Initialize FaceMesh
   face = mp_face_mesh.FaceMesh(
       static_image_mode=False,
       max_num_faces=1,
       refine_landmarks=True,
       min_detection_confidence=0.5
   )

   # Open camera
   picam2 = Picamera2()
   config = picam2.create_preview_configuration(
      main={"size": (640, 480), "format": "XRGB8888"} ,
   )
   picam2.configure(config)
   picam2.start()

   print("Streaming... press 'q' to quit")

   while True:
       frame_bgra = picam2.capture_array()
       frame_bgr  = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)

       frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
       results = face.process(frame)
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

       if results.multi_face_landmarks:
           for face_landmarks in results.multi_face_landmarks:
               drawing.draw_landmarks(
                   image=frame,
                   landmark_list=face_landmarks,
                   connections=mp_face_mesh.FACEMESH_TESSELATION,
                   landmark_drawing_spec=drawing.DrawingSpec(thickness=1, circle_radius=1),
                   connection_drawing_spec=drawing_styles.get_default_face_mesh_tesselation_style()
               )

               # --------- Emotion detection ---------
               label, metrics = classify_emotion(face_landmarks.landmark)

               # Draw emotion label on the frame
               cv2.putText(frame, f"Emotion: {label}", (20, 40),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2, cv2.LINE_AA)

               # Debug information
               dbg = f"mw:{metrics.get('mouth_width',0)} mo:{metrics.get('mouth_open',0)} eo:{metrics.get('eye_open',0)}"
               cv2.putText(frame, dbg, (20, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1, cv2.LINE_AA)

       cv2.imshow("Show Video", frame)
       if cv2.waitKey(1) & 0xff == ord('q'):
           break

   picam2.stop_preview()
   picam2.stop()
   cv2.destroyAllWindows()

プログラムを実行すると、カメラ映像上に認識された表情カテゴリがリアルタイムで表示されます。  
また、口の幅・口の開き具合・目の開き具合などのデバッグ情報も同時に表示されます。

-----------------------------
5. 主要ステップの解説
-----------------------------

#. 重要な特徴点の選択

   .. code-block:: python

      # Keypoint Index (MediaPipe 468 points)
      L_EYE_TOP, L_EYE_BOT = 159, 145
      R_EYE_TOP, R_EYE_BOT = 386, 374
      L_EYE_CENTER, R_EYE_CENTER = 33, 263
      MOUTH_LEFT, MOUTH_RIGHT = 61, 291
      LIP_UP, LIP_DOWN = 13, 14

   これらのインデックスは次の部位に対応します：

   - 159, 145 → 左目の上端と下端  
   - 386, 374 → 右目の上端と下端  
   - 33, 263 → 両目の中心（正規化に使用）  
   - 61, 291 → 口角  
   - 13, 14 → 上唇と下唇の中央  

   .. image:: img/mp_face_point.jpg
      :align: center

#. 距離の正規化

   カメラとの距離の影響を小さくするため、  
   両目の中心間の距離を正規化スケールとして使用します。

   .. code-block:: python

      def euclidean(p1, p2):
          return np.linalg.norm(
              np.array([p1.x, p1.y]) -
              np.array([p2.x, p2.y])
          )

      io = euclidean(
          landmarks[L_EYE_CENTER],
          landmarks[R_EYE_CENTER]
      )

#. 幾何特徴の計算

   .. code-block:: python

      mouth_width = euclidean(
          landmarks[MOUTH_LEFT],
          landmarks[MOUTH_RIGHT]
      ) / io

      mouth_open = euclidean(
          landmarks[LIP_UP],
          landmarks[LIP_DOWN]
      ) / io

      eye_open_L = euclidean(
          landmarks[L_EYE_TOP],
          landmarks[L_EYE_BOT]
      ) / io

      eye_open_R = euclidean(
          landmarks[R_EYE_TOP],
          landmarks[R_EYE_BOT]
      ) / io

      eye_open = 0.5 * (eye_open_L + eye_open_R)

   計算される特徴量：

   - ``mouth_width`` → 口の横幅
   - ``mouth_open`` → 口の縦方向の開き具合
   - ``eye_open`` → 両目の平均的な開き具合

#. 閾値を用いた表情分類

   .. code-block:: python

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

   表情判定ルール（経験的な閾値）：

   - Surprised → 口と目が大きく開いている
   - Happy → 口が大きく開き、目は通常の状態
   - Sad / Angry → 口と目が比較的閉じている
   - Neutral → 上記のどの条件にも当てはまらない

-----------------------------------------------------
6. 閾値とロバスト性の調整
-----------------------------------------------------

- ``0.08`` 、 ``0.035`` 、 ``0.018`` などの閾値は、640×480 解像度での経験値に基づいています。  
- カメラ距離や解像度が異なる場合は、デバッグ情報（mw/mo/eo）を参考に調整してください。  
- より高精度にする場合は、口角位置や口形状などの特徴を追加したり、学習済みモデルを使用することも可能です。

------------------------------------------------------------
7. トラブルシューティング
------------------------------------------------------------

- 表情認識の感度が低い

  閾値が現在のカメラ距離に適していない可能性があります。  
  ``mouth_open`` や ``eye_open`` の値を調整してください。

- 検出が遅い

  解像度が高すぎる可能性があります。  
  解像度を下げるか ``refine_landmarks`` を無効にしてください。

- 表情が認識されない

  照明が不足している、または顔の角度が傾いている可能性があります。  
  照明を改善し、カメラに正面を向けてください。

-----------------------------
8. まとめ
-----------------------------

- 本章では **幾何特徴 + FaceMesh ランドマーク** を利用した軽量な表情認識を実装しました。  
- **高いリアルタイム性能** と **調整可能な閾値** が特徴です。  
- インタラクティブアート、HCI、授業や会議の状態検出などのプロジェクトに応用できます。  