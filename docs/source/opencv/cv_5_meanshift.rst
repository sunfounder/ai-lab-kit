.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

5. Seguimiento de Objetos con MeanShift
===========================================

MeanShift es un algoritmo clásico de seguimiento de objetos basado en histogramas.
En esta lección, no solo implementaremos un ejemplo completo de **seguimiento con MeanShift**, sino que también explicaremos **por qué** se realiza cada paso y **qué sucede internamente**.

.. raw:: html

      <video width="400" loop muted controls>
          <source src="../_static/video/Opencv_5.mp4" type="video/mp4">
          Your browser does not support the video tag.
      </video>

1. ¿Qué es MeanShift?
-------------------------

MeanShift desplaza iterativamente una ventana según la densidad de probabilidad para **encontrar la ubicación más probable del objetivo**.

En palabras simples:
Primero le das al algoritmo una "región objetivo inicial". Calcula las características de color de esta región (por ejemplo, el histograma de color del objetivo), y luego en cada fotograma subsiguiente encuentra el área más similar a ese color y mueve el rectángulo hacia allí.

Este proceso no depende del aprendizaje profundo y no requiere preentrenamiento, es muy ligero.

.. image:: img/opencv_meanshift.png
   :alt: Seguimiento MeanShift
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
      python3 cv_5_meanshift.py

#. Cuando ejecutes el programa, aparecerá una ventana de OpenCV llamada **MeanShift Tracker** y comenzará a reproducir el archivo de video ``sample2.mp4``.

   Se dibujará un rectángulo verde alrededor del objeto objetivo y se actualizará en tiempo real utilizando el algoritmo de seguimiento MeanShift.

   La ventana de seguimiento se moverá a medida que el objeto se mueva en el video.

   Puedes salir del programa de dos maneras:

   * Presionar la tecla **q** en el teclado
   * Cerrar la ventana haciendo clic en el botón de cerrar (X)

   Después de salir, la reproducción del video se detiene y todas las ventanas de OpenCV se cierran.

3. Código Completo
-----------------------

A continuación se muestra el script completo de seguimiento MeanShift (``cv_5_meanshift.py``):

.. code-block:: python

   import numpy as np
   import cv2

   cap = cv2.VideoCapture("sample2.mp4")

   # Read the first frame
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the video file.")

   # Initial tracking window (x, y, w, h)
   x, y, w, h = 80, 100, 80, 80
   track_window = (x, y, w, h)

   # Convert the first frame to HSV
   hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   # Extract ROI in HSV (ONLY the selected area)
   roi_hsv = hsv_frame[y:y+h, x:x+w]

   # Create a mask for ROI (filter out low saturation/value pixels)
   roi_mask = cv2.inRange(
      roi_hsv,
      np.array((0, 61, 33), dtype=np.uint8),
      np.array((180, 255, 255), dtype=np.uint8)
   )

   # Compute histogram of ROI (Hue channel)
   roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])

   # Normalize histogram for better tracking
   cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   # Termination criteria: max 15 iterations or move by at least 2 pixels
   termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   # FPS settings (fallback if FPS is unavailable)
   fps = cap.get(cv2.CAP_PROP_FPS)
   if not fps or fps <= 1e-3:
      fps = 30.0
   delay_ms = int(1000 / fps)

   WINDOW_NAME = "MeanShift Tracker"

   while True:
      ret, frame = cap.read()

      # Loop video
      if not ret:
         cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
         continue

      # Convert frame to HSV
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      # Back projection: probability map of where the ROI histogram appears in the frame
      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

      # Apply meanShift to update tracking window
      _, track_window = cv2.meanShift(bp, track_window, termination)

      # Draw tracking window
      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
      cv2.putText(frame, "MeanShift Tracker", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

      cv2.imshow(WINDOW_NAME, frame)

      # Handle keyboard input and GUI events
      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
         break

      # Exit if window is closed
      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
         break

   cap.release()
   cv2.destroyAllWindows()

4. Explicación
---------------------------

#. Abrir el archivo de video:

   .. code-block:: python

      cap = cv2.VideoCapture("sample2.mp4")

   Esto crea un objeto de captura de video para que OpenCV pueda leer fotogramas del archivo.

#. Leer el primer fotograma y asegurarse de que funcione:

   .. code-block:: python

      ret, frame = cap.read()
      if not ret:
          raise RuntimeError("Cannot read the video file.")

   El seguimiento MeanShift necesita un fotograma inicial para aprender qué rastrear.

#. Establecer la ventana de seguimiento inicial (el objeto que deseas rastrear):

   .. code-block:: python

      x, y, w, h = 80, 100, 80, 80
      track_window = (x, y, w, h)

   Este rectángulo es la posición inicial del objetivo (ROI).
   Generalmente ajustas estos valores para que coincidan con el objeto en el primer fotograma.

#. Convertir el primer fotograma a HSV y extraer el ROI:

   .. code-block:: python

      hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      roi_hsv = hsv_frame[y:y+h, x:x+w]

   HSV se usa comúnmente para el seguimiento porque el canal de Tono describe el color de manera más consistente que RGB/BGR.

#. Construir una máscara para ignorar píxeles débiles/inválidos en el ROI:

   .. code-block:: python

      roi_mask = cv2.inRange(
          roi_hsv,
          np.array((0, 61, 33), dtype=np.uint8),
          np.array((180, 255, 255), dtype=np.uint8)
      )

   Esto filtra los píxeles con saturación/valor muy bajos (a menudo sombras o ruido), mejorando la estabilidad del seguimiento.

#. Calcular y normalizar el histograma del ROI (canal Tono):

   .. code-block:: python

      roi_hist = cv2.calcHist([roi_hsv], [0], roi_mask, [180], [0, 180])
      cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

   - El histograma describe la distribución de color del objetivo (Tono).
   - La normalización hace que la escala del histograma sea consistente en diferentes condiciones de iluminación o tamaños de ROI.

#. Definir los criterios de terminación para MeanShift:

   .. code-block:: python

      termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 2)

   MeanShift se detendrá cuando:
   - se ejecuten 15 iteraciones, o
   - el movimiento de la ventana sea menor de 2 píxeles.

#. Establecer un retardo de reproducción basado en los FPS del video:

   .. code-block:: python

      fps = cap.get(cv2.CAP_PROP_FPS)
      if not fps or fps <= 1e-3:
          fps = 30.0
      delay_ms = int(1000 / fps)

   Esto mantiene la reproducción cerca de la velocidad original del video.
   Si no se pueden leer los FPS, se usa 30 FPS como valor predeterminado.

#. Convertir cada fotograma a HSV (para el seguimiento):

   .. code-block:: python

      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   El seguimiento se realiza en HSV para que podamos coincidir con el histograma de Tono del objetivo.

#. Proyección inversa (encontrar dónde es probable que esté el color del objetivo):

   .. code-block:: python

      bp = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], scale=1)

   La proyección inversa produce un mapa de probabilidad: las áreas brillantes tienen más probabilidades de coincidir con el histograma del ROI.

#. Actualizar la ventana de seguimiento usando MeanShift:

   .. code-block:: python

      _, track_window = cv2.meanShift(bp, track_window, termination)

   MeanShift mueve la ventana de seguimiento hacia el área de mayor densidad en el mapa de probabilidad, actualizando la posición del objetivo fotograma a fotograma.

#. Dibujar el resultado del seguimiento:

   .. code-block:: python

      x, y, w, h = track_window
      cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

   Esto dibuja el rectángulo de seguimiento actual en el fotograma del video.

#. Mostrar la ventana y condiciones de salida:

   .. code-block:: python

      key = cv2.waitKey(delay_ms) & 0xFF
      if key == ord("q"):
          break

      if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
          break

   - Presiona ``q`` para salir.
   - Cerrar la ventana también sale de forma segura.

#. Liberar recursos:

   .. code-block:: python

      cap.release()
      cv2.destroyAllWindows()

   Siempre libera el video y cierra las ventanas para liberar recursos del sistema.

5. MeanShift vs. CAMShift
----------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Característica
     - MeanShift
     - CAMShift
   * - Tamaño de ventana
     - Fijo
     - Se ajusta automáticamente (se adapta a la escala del objetivo)
   * - Objetivo en rotación
     - No compatible
     - Compatible
   * - Escenarios adecuados
     - Tamaño del objetivo relativamente estable
     - El objetivo puede escalar/rotar
   * - Aplicaciones
     - Seguimiento simple, pelotas, marcadores
     - Seguimiento práctico, vigilancia, reconocimiento


6. Avanzado: Seleccionar ROI con el Ratón
--------------------------------------

Anteriormente, usamos valores fijos:

.. code-block:: python

   x, y, w, h = 150, 200, 80, 80

Eso es simple pero no flexible.
Si cambias de video o el objetivo comienza en otro lugar, tendrías que modificar el código.

OpenCV proporciona ``cv2.selectROI`` para que puedas **seleccionar la región objetivo de forma interactiva en el primer fotograma** con el ratón, y el programa obtendrá ``(x, y, w, h)`` automáticamente.

**Código de inicialización modificado**

Ejecuta ``cv_5_meanshift_auto.py`` para el código modificado.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py


.. code-block:: python
   :emphasize-lines: 24,25

   import numpy as np
   import cv2
   from pathlib import Path

   # -----------------------------
   # Load video
   # -----------------------------
   BASE_DIR = Path(__file__).resolve().parent
   video_path = str(BASE_DIR / "sample3.mp4")

   cap = cv2.VideoCapture(video_path)
   if not cap.isOpened():
      raise RuntimeError("Error opening video file")

   # Read the first frame (needed for ROI selection and building the target model)
   ret, frame = cap.read()
   if not ret:
      raise RuntimeError("Cannot read the first frame from the video")

   # -----------------------------
   # Select ROI with mouse
   # -----------------------------
   # Press Enter/Space to confirm, press Esc to cancel
   roi_box = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
   cv2.destroyWindow("Select ROI")
   ...

Cuando ejecutes el programa, se mostrará el primer fotograma del video y se te pedirá que selecciones una Región de Interés (ROI) usando el ratón.

Arrastra el ratón para dibujar un rectángulo alrededor del objeto objetivo, luego presiona **Enter** o **Espacio** para confirmar la selección.
Presiona **Esc** para cancelar la selección.

Después de confirmar la ROI, aparecerá una ventana llamada **MeanShift Tracker**.
El objeto seleccionado será rastreado con un rectángulo verde, y el rectángulo se moverá a medida que el objeto se mueva en el video.

Para detener el programa:

* Presiona la tecla **q** en el teclado
* O cierra la ventana de visualización usando el botón de cerrar (X)

Después de salir, la reproducción del video se detiene y todas las ventanas de OpenCV se cierran.

.. image:: img/opencv_meanshift_mouse.png
   :alt: Ventana de selección interactiva de ROI
   :align: center

**Notas**

``cv2.selectROI`` es el selector ROI interactivo integrado de OpenCV, ideal para la inicialización manual.
Devuelve ``(x, y, w, h)``, que es totalmente compatible con ``track_window``, por lo que no necesitas cambiar la lógica principal de CAMShift/MeanShift.
Esto te permite reutilizar el mismo programa en diferentes videos y objetivos.


7. Avanzado II: Calcular Dinámicamente los Umbrales HSV para el ROI
--------------------------------------------------------------

El ``cv_5_meanshift.py`` original utiliza umbrales HSV establecidos manualmente, adecuados cuando el color del objetivo es fijo y la iluminación es estable.


.. code-block:: python

   # apply mask on the HSV frame
   roi_mask = cv2.inRange(roi_hsv, lower, upper)

Si la iluminación varía significativamente o el color del objetivo no es fijo, los límites ``inRange`` codificados pueden ser subóptimos.
Un enfoque más inteligente es **calcular automáticamente los límites superior e inferior HSV a partir del ROI seleccionado**.

**Ejemplo: Cálculo automático de umbrales HSV**

Ejecuta ``cv_5_meanshift_auto.py`` para el código modificado.

.. code-block:: bash

   cd ~/ai-lab-kit/opencv_python
   python3 cv_5_meanshift_auto.py

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


Al seleccionar objetivos muy oscuros o muy brillantes, ya no necesitas ajustar los umbrales manualmente; también se adapta rápidamente a diferentes condiciones de iluminación y colores.

.. note::

   - ``np.percentile`` (5%–95%) recorta los extremos (bordes, sombras, reflejos, etc.) dentro del ROI, mejorando la robustez.
   - ``pad_h``, ``pad_s``, ``pad_v`` proporcionan tolerancia para que los cambios de color leves aún sean capturados.
   - ``lower`` y ``upper`` son los límites HSV dinámicos utilizados directamente con ``cv2.inRange``.


**Resumen**

- Usa ``cv2.selectROI`` para una inicialización flexible del objetivo.
- Usa ``np.percentile`` para calcular automáticamente los límites HSV y adaptarse.
- Combinado con ``cv2.inRange`` y CAMShift/MeanShift, este enfoque se mantiene estable bajo condiciones de iluminación desafiantes y variaciones del objetivo.
