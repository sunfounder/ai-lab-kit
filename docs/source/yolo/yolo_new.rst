.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Ejecutar YOLO en Raspberry Pi
==============================================================

YOLO (You Only Look Once) es un algoritmo revolucionario de deteccion de objetos caracterizado por su velocidad y precision. Transforma la deteccion de objetos en un problema de regresion, prediciendo todas las categorias y ubicaciones de objetos en una imagen a traves de una unica pasada directa de una red neuronal.

Imaginalo como un sistema de vision que puede "ver todo de un vistazo". Ya sea en vigilancia por video, conduccion autonoma o inspeccion de calidad industrial, YOLO se encuentra dondequiera que se necesite deteccion de objetos en tiempo real.

.. image:: img/yolo_new.png

Figura: YOLOv8n ejecutandose en tiempo real en Raspberry Pi. Los objetos en el feed de la camara se detectan y anotan con precision, mostrando las clases detectadas y las puntuaciones de confianza a la izquierda. Esta imagen muestra el modelo identificando correctamente objetos como una persona, una silla y un televisor.

Principios Fundamentales
------------------------------------------

A diferencia de los metodos anteriores de dos etapas (como R-CNN) que "primero encuentran regiones candidatas y luego las identifican", YOLO adopta un enfoque fundamentalmente diferente:

* **Marco Unificado**: Divide la imagen en una cuadricula (por ejemplo, la cuadricula original de 7x7).

* **Prediccion de Cuadricula**: Cada celda de la cuadricula es responsable de predecir objetos cuyo centro cae dentro de esa celda. Cada cuadricula predice multiples cuadros delimitadores (incluyendo posicion y tamano) junto con sus puntuaciones de confianza, mientras tambien predice probabilidades de clase del objeto.

* **Finalizacion en Una Etapa**: La clasificacion y la localizacion se realizan simultaneamente dentro de la misma red neuronal, logrando realmente "you only look once", superando asi significativamente a metodos anteriores en velocidad.


Ejecutar el Codigo
------------------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_test.py

El codigo descargara automaticamente un modelo (aproximadamente 6 MB) y lo ejecutara en la camara. Los resultados se mostraran en una ventana con el titulo "YOLOv8".

(la primera ejecucion descargara automaticamente un modelo de aproximadamente 6 MB):

.. code-block:: python

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("yolov8n.pt")  # nano model

   # initialize camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLO start, Press 'q' to exit...")

   try:
      while True:
         # capture frame
         frame = picam2.capture_array()

         # run YOLO and set imgsz=320
         results = model(frame, imgsz=320)

         # draw results
         annotated = results[0].plot()

         # show results
         cv2.imshow("YOLO on Raspberry Pi", annotated)

         # press 'q' to exit
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("exit")



Solucion de Problemas
---------------

P: Si encuentras el error Numpy.dtype size changed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cambia a una version anterior de Numpy:

.. code-block:: bash

   # If version is 2.x, downgrade to 1.x
   pip3 install "numpy<2.0" --break-system-packages --force-reinstall

P: Si encuentras el error ``libopenblas.so.0`` faltante
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instala la libreria OpenBLAS:

.. code-block:: bash

   sudo apt install libopenblas-dev

P: Si la camara no se puede abrir
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verifica la conexion de la camara y asegurate de que este habilitada:

.. code-block:: bash

   sudo raspi-config
   # Select Interface Options -> Camera -> Enable

P: Si encuentras errores de falta de memoria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aumenta el espacio de intercambio:

.. code-block:: bash

   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Modify CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon

Metodos de Optimizacion de Rendimiento
--------------------------------------------------------

Ejecutar YOLO en una Raspberry Pi (incluso 4B/5) puede ser exigente. Aqui hay varios metodos de optimizacion probados:

1. **Ajustar la Resolucion de Inferencia de YOLO**: El codigo anterior ya usa imgsz=320, que es una configuracion equilibrada. Valores ajustables:

   * ``imgsz=224`` - Resolucion mas baja, maxima velocidad
   * ``imgsz=320`` - Opcion estandar
   * ``imgsz=416`` - Mayor precision, velocidad mas lenta
   * ``imgsz=640`` - Maxima precision, muy lento en Raspberry Pi

2. **Elegir el Modelo Adecuado**:

   * ``yolov8n.pt`` (6MB) - Mas rapido, adecuado para deteccion en tiempo real
   * ``yolov8s.pt`` (22MB) - Un poco mas lento pero mas preciso
   * ``yolov8m.pt`` (49MB) - Mas lento, mayor precision
   * ``yolov8l/x.pt`` - Generalmente no usable en Raspberry Pi
   * Tambien puedes usar tu propio modelo entrenado, por ejemplo, ``"/home/pi/my_model.pt"``. Cubriremos como entrenar modelos personalizados en capitulos posteriores.

3. **Limitar las Clases de Deteccion**: Si solo se detectan objetos especificos (por ejemplo, solo personas), modifica el codigo:

.. code-block:: python

   results = model(frame, classes=[0], imgsz=320)  # 0 is the class ID for person

IDs de clase comunes:

   * 0 - person
   * 1 - bicycle
   * 2 - car
   * 3 - motorcycle
   * 5 - bus
   * 7 - truck

4. **Usar Variantes de Modelo Ligero**:

.. code-block:: python

   # Use pruned version of YOLOv8n (if available)
   model = YOLO("yolov8n.pt")

   # Or use TensorRT acceleration (requires additional configuration)
   # model = YOLO("yolov8n.pt")
   # model.export(format="engine")  # Export as TensorRT engine

5. **Reducir el Procesamiento de Fotogramas**: Si no es necesario mostrar todos los fotogramas en tiempo real, procesalos de forma intermitente:

.. code-block:: python

   frame_count = 0
   while True:
       frame = picam2.capture_array()

       # Process every 3rd frame
       if frame_count % 3 == 0:
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           cv2.imshow("YOLO on Raspberry Pi", annotated)

       frame_count += 1

       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

6. **Usar Multihilos**: Separa la captura de la camara y la inferencia de YOLO en diferentes hilos:

.. code-block:: python

   import threading
   import queue

   frame_queue = queue.Queue(maxsize=2)
   result_queue = queue.Queue(maxsize=2)

   def capture_frames():
       while True:
           frame = picam2.capture_array()
           if frame_queue.full():
               frame_queue.get()
           frame_queue.put(frame)

   def process_frames():
       while True:
           frame = frame_queue.get()
           results = model(frame, imgsz=320)
           annotated = results[0].plot()
           if result_queue.full():
               result_queue.get()
           result_queue.put(annotated)

   # Start threads
   threading.Thread(target=capture_frames, daemon=True).start()
   threading.Thread(target=process_frames, daemon=True).start()

   while True:
       if not result_queue.empty():
           cv2.imshow("YOLO on Raspberry Pi", result_queue.get())
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

Uso Avanzado
--------------------------------

Usar Archivos de Video como Entrada
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import cv2
   from ultralytics import YOLO

   model = YOLO("yolov8n.pt")
   cap = cv2.VideoCapture("input_video.mp4")

   while cap.isOpened():
       ret, frame = cap.read()
       if not ret:
           break

       results = model(frame, imgsz=320)
       annotated = results[0].plot()
       cv2.imshow("YOLO Detection", annotated)

       if cv2.waitKey(1) & 0xFF == ord('q'):
           break

   cap.release()
   cv2.destroyAllWindows()

Resumen
------------------

A traves de este tutorial, has aprendido:

* Como configurar el entorno YOLO en Raspberry Pi
* Como realizar deteccion de objetos en tiempo real usando la camara
* Como resolver problemas comunes de instalacion y ejecucion
* Varios metodos para optimizar el rendimiento de deteccion

El poder de YOLO radica en su simplicidad y eficiencia, permitiendo un rendimiento de deteccion de objetos respetable incluso en dispositivos integrados como la Raspberry Pi. Continua explorando y podras construir varias aplicaciones interesantes como vigilancia inteligente, seguimiento de objetos y conteo de personas.
