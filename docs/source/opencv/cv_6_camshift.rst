.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

6. Seguimiento de Objetos con CAMShift
=========================================

En el capítulo anterior, aprendimos el algoritmo MeanShift, que puede rastrear continuamente un objetivo en un video basándose en su histograma de color.
En esta sección, presentamos **CAMShift (Continuously Adaptive Mean Shift)**,
que extiende MeanShift **adaptando automáticamente el tamaño y la orientación de la ventana**, haciéndolo más práctico para aplicaciones del mundo real.
Además, en este ejemplo rastrearemos un objetivo **basándonos en el brillo en lugar del color**, lo que también es muy común en la práctica.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_6.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. Características del Algoritmo
---------------------

**MeanShift** solo puede rastrear la posición del objetivo y utiliza una ventana de tamaño fijo.
**CAMShift** rastrea la posición **y** ajusta automáticamente el tamaño y el ángulo de la ventana.

Por ejemplo, cuando el objetivo se acerca a la cámara, el cuadro de seguimiento crece; cuando el objetivo se aleja, se reduce; cuando el objetivo rota, el cuadro rota en consecuencia.

.. image:: img/opencv_camshift.png
   :alt: Ilustración del seguimiento CAMShift
   :align: center


2. Ejecutar el Código
------------------------

.. important::

   Antes de comenzar, asegúrate de:

   * Tener el soporte para cámara ensamblado
   * Poder acceder al escritorio de Raspberry Pi
   * Tener el paquete de código instalado
   * Tener Fusion HAT+ instalado y configurado
   * Tener OpenCV instalado

   Para obtener instrucciones detalladas, consulta :ref:`opencv_install`.

#. Abre la terminal e ingresa el siguiente comando:

   .. code-block:: bash

      cd ~/ai-lab-kit/opencv_python
      python3 cv_6_camshift.py

#. Cuando ejecutes el programa, aparecerá una ventana de OpenCV llamada **CAMShift Tracker** y comenzará a reproducir el archivo de video *sample3.mp4*.

   El programa rastrea al gato negro usando el algoritmo CAMShift (Continuously Adaptive Mean Shift).

   Se dibujará un rectángulo verde rotado alrededor del objeto rastreado.
   A medida que el gato se mueve o cambia su tamaño y orientación, la ventana de seguimiento adaptará automáticamente su posición, tamaño y ángulo.

   Puedes salir del programa de dos maneras:

   * Presionar la tecla **q** en el teclado
   * Cerrar la ventana haciendo clic en el botón de cerrar (X)

   Después de salir, la reproducción del video se detiene y todas las ventanas de OpenCV se cierran.

3. Código Completo
---------------------

Abre ``cv_6_camshift.py`` para ver el código completo.

.. code-block:: python

   # Python program to demonstrate CAMShift (tracking a dark object)
   import numpy as np
   import cv2

   # Read video
   cap = cv2.VideoCapture("sample3.mp4")

   # Retrieve the first frame from the video
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Set the initial region for tracking window (x, y, width, height)
   x, y, w, h = 100, 200, 40, 40
   track_window = (x, y, w, h)

   # Convert first frame to HSV
   hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI (only the target area) in HSV
   hsv_roi = hsv[y:y+h, x:x+w]

   # For tracking a black object, we keep dark pixels (low V) inside ROI
   # V channel is hsv[..., 2], so we build a mask based on V <= 80
   roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   # Build histogram on V channel (channel index 2) within ROI
   # Use 256 bins for V (0~256) to match back projection range
   roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria for CAMShift
   term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   # FPS delay (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "CAMShift Tracker"

   while True:
      ret, frame = cap.read()

      # If video ends, restart from beginning
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection on V channel using ROI histogram (range 0~256)
      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

      # Apply CAMShift
      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

      # Draw rotated rectangle
      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

      cv2.putText(frame, "CAMShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Keyboard + GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if user closes the window (click X)
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Explicación del Código
---------------------------

#. Abrir el archivo de video y leer el primer fotograma:

   .. code-block:: python

      cap = cv2.VideoCapture("sample3.mp4")
      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   CAMShift necesita un fotograma inicial para aprender qué rastrear.

#. Establecer la ventana de seguimiento inicial (ROI):

   .. code-block:: python

      x, y, w, h = 100, 200, 40, 40
      track_window = (x, y, w, h)

   Este rectángulo debe cubrir el objeto objetivo en el primer fotograma.
   CAMShift actualizará esta ventana automáticamente durante el seguimiento.

#. Convertir el primer fotograma a HSV y extraer el ROI:

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      hsv_roi = hsv[y:y+h, x:x+w]

   HSV es conveniente para el seguimiento porque puedes elegir canales específicos (como V para el brillo).

#. Construir una máscara para un objeto oscuro (valores bajos de V):

   .. code-block:: python

      roi_mask = cv2.inRange(hsv_roi, np.array((0, 0, 0)), np.array((180, 255, 80)))

   Esto mantiene solo los píxeles "oscuros" en el ROI.
   Para objetos negros/oscuros, el brillo (V) suele ser la característica más útil.

#. Calcular y normalizar un histograma del canal V:

   .. code-block:: python

      roi_hist = cv2.calcHist([hsv_roi], [2], roi_mask, [256], [0, 256])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - El canal ``2`` significa el canal **V (Valor/brillo)** en HSV.
   - El histograma describe qué tan "oscuro/brillante" es el ROI del objetivo.
   - La normalización hace que el seguimiento sea más estable.

#. Establecer los criterios de terminación para CAMShift:

   .. code-block:: python

      term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

   CAMShift deja de actualizarse cuando alcanza 10 iteraciones o el movimiento es menor de 1 píxel.

#. Establecer la velocidad de reproducción usando FPS:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Esto establece un retardo para que el video se reproduzca cerca de sus FPS originales.

#. Crear un mapa de probabilidad usando proyección inversa (canal V):

   .. code-block:: python

      back_proj = cv2.calcBackProject([hsv], [2], roi_hist, [0, 256], 1)

   La proyección inversa resalta los píxeles en el fotograma cuyos valores V coinciden con el histograma del ROI.
   Los valores más brillantes en ``back_proj`` significan "más probable que sea el objetivo".

#. Rastrear usando CAMShift y actualizar la ventana:

   .. code-block:: python

      rot_rect, track_window = cv2.CamShift(back_proj, track_window, term_crit)

   CAMShift se basa en MeanShift, pero también puede adaptar el **tamaño y la rotación** de la ventana de seguimiento.

   - ``track_window`` se actualiza en cada fotograma.
   - ``rot_rect`` contiene un rectángulo rotado (centro, tamaño, ángulo).

#. Dibujar el cuadro de seguimiento rotado:

   .. code-block:: python

      pts = cv2.boxPoints(rot_rect).astype(np.int32)
      cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

   Esto convierte el rectángulo rotado en cuatro puntos de esquina y lo dibuja en el fotograma.

#. Condiciones de salida (teclado + cierre de ventana):

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   Presiona ``q`` para salir, o cierra la ventana para detenerte de forma segura.

#. Liberar recursos:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Siempre libera el archivo de video y cierra las ventanas al final.


5. CAMShift vs. MeanShift
--------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Característica
     - MeanShift
     - CAMShift
   * - Tamaño de ventana
     - Fijo
     - Adaptativo
   * - Ángulo
     - No compatible
     - Soporta rotación
   * - Precisión de seguimiento
     - Moderada
     - Mayor, más adaptativo
   * - Aplicaciones
     - Objetos estáticos
     - Movimiento complejo, objetivos rotatorios

CAMShift es una mejora sobre MeanShift,
manejando mejor la deformación del objetivo, la rotación y los cambios de distancia, siendo muy adecuado para escenarios del mundo real.

6. Extensiones y Práctica
-------------------------------------------

- Ajusta los umbrales ``inRange`` para rastrear objetivos verdes o azules
- Combínalo con la entrada de cámara en vivo para construir un sistema de seguimiento basado en color en tiempo real


7. Avanzado: Selección Interactiva de ROI y Ajuste Automático de Umbrales HSV
-------------------------------------------------------------------------

Como en la sección anterior, este proyecto también puede usar la interacción con el ratón para seleccionar el ROI y ajustar automáticamente los umbrales HSV.

Ejecuta ``cv_6_camshift_auto.py`` para el código modificado.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_6_camshift_auto.py

Cuando ejecutes el programa, se mostrará el primer fotograma del video y se te pedirá que selecciones una Región de Interés (ROI) con el ratón.

Arrastra el ratón para dibujar un rectángulo alrededor del objeto objetivo, luego presiona **Enter** o **Espacio** para confirmar la selección.
Presiona **Esc** para cancelar la selección.

Después de seleccionar la ROI, aparecerá una ventana llamada **CAMShift Tracker**.
El objeto seleccionado será rastreado con un rectángulo verde rotado, y la ventana de seguimiento adaptará automáticamente su posición, tamaño y orientación a medida que el objeto se mueva.

Para detener el programa:

* Presiona la tecla **q** en el teclado
* O cierra la ventana de visualización usando el botón de cerrar (X)

Después de salir, la reproducción del video se detiene y todas las ventanas de OpenCV se cierran.


.. code-block:: python

   hsv0 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
   roi_hsv = hsv0[y:y + h, x:x + w]

   # Split ROI HSV channels
   h_roi = roi_hsv[:, :, 0]
   s_roi = roi_hsv[:, :, 1]
   v_roi = roi_hsv[:, :, 2]

   # Use percentiles to get robust ranges (ignore outliers)
   h_low, h_high = np.percentile(h_roi, [5, 95])
   s_low, s_high = np.percentile(s_roi, [5, 95])
   v_low, v_high = np.percentile(v_roi, [5, 95])

   # Add padding so the range is not too tight
   pad_h, pad_s, pad_v = 10, 20, 20

   lower = np.array([
      max(int(h_low) - pad_h, 0),
      max(int(s_low) - pad_s, 0),
      max(int(v_low) - pad_v, 0)
   ], dtype=np.uint8)

   upper = np.array([
      min(int(h_high) + pad_h, 180),
      min(int(s_high) + pad_s, 255),
      min(int(v_high) + pad_v, 255)
   ], dtype=np.uint8)

   # Mask ONLY the ROI (do not use the whole frame mask)
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

   ...
