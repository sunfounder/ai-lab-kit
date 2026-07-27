.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Entrenar tu Propio Modelo YOLO
=====================================

Entrenar tu propio modelo YOLO esencialmente implica dejar que el algoritmo de aprendizaje profundo aprenda como identificar objetos especificos a partir de los datos de imagen que proporcionas. Este proceso se puede analogizar a ensenar a un nino a reconocer algo nuevo: le muestras numerosas imagenes de ejemplo desde diferentes angulos y entornos, diciendole "este es el objeto objetivo". Despues de suficientes ejemplos, puede identificar con precision ese objeto en nuevas imagenes.

Para YOLO, el proceso de entrenamiento funciona asi:

1. **Preparacion de Datos**: Recopila imagenes que contengan los objetos objetivo y anota la posicion y categoria de cada objeto
2. **Aprendizaje del Modelo**: El algoritmo aprende automaticamente los patrones de caracteristicas de los objetos analizando estos datos anotados
3. **Generacion de Pesos**: Despues de completar el entrenamiento, genera un archivo de modelo (archivo .pt) que contiene el conocimiento aprendido
4. **Aplicacion de Inferencia**: Implementa este modelo en la Raspberry Pi para la deteccion en nuevas imagenes

Gracias al aprendizaje por transferencia, no necesitamos entrenar desde cero. La plataforma Ultralytics proporciona modelos base preentrenados (como YOLOv8n) que han sido entrenados con millones de imagenes. Solo necesitamos "ajustar" estos modelos con una pequena cantidad de nuestras propias imagenes para crear modelos personalizados efectivos.



----------------------------------------------------------

Capturar Fotos
------------------------------

Dado que nuestro proyecto YOLO esta basado en la Raspberry Pi, usaremos la camara de la Raspberry Pi para capturar fotos. Para obtener mejores resultados, tambien usamos telefonos moviles para capturar algunas fotos y aumentar la diversidad de datos.

**Consejos para la Captura de Fotos**

* **Nitidez**: Captura los objetos lo mas claramente posible, evitando borrosidad
* **Diversidad**: Captura fotos desde diferentes angulos (frontal, lateral, superior, etc.) y bajo diferentes condiciones de iluminacion (luz brillante, poca luz, contraluz, etc.)
* **Variacion de Fondo**: Intenta capturar imagenes con diferentes fondos para ayudar al modelo a aprender las caracteristicas esenciales de los objetos en lugar de los fondos
* **Evitar Superposiciones**: Puedes capturar varios objetos simultaneamente, pero evita superposiciones significativas entre objetos
* **Cantidad Recomendada**: Apunta a al menos 50-100 fotos por categoria; mas imagenes producen mejores resultados

**¿Que Objeto Deberias Usar?**

Puedes elegir cualquier objeto que te interese para entrenar, como: un muneco, una taza, una silla o incluso tu mascota. Este tutorial utiliza un muneco de muneco de nieve como ejemplo; simplemente reemplazalo con tu propio objeto objetivo.

.. image:: img/ultralytics_a1_capture_photo.png

**Capturar Fotos con la Camara de Raspberry Pi**

Aqui esta el codigo para capturar fotos usando la camara de Raspberry Pi:

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_capture_images.py

.. code-block:: python

   #!/usr/bin/env python3
   """
   Simple camera capture script for Raspberry Pi
   Press SPACE to capture, ESC to exit
   Images saved to ./captured_images/
   """

   from picamera2 import Picamera2
   import cv2
   import os
   import time

   # Create save directory
   save_dir = "captured_images"
   os.makedirs(save_dir, exist_ok=True)

   # Initialize camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   # Wait for camera to warm up
   time.sleep(1)

   print("=== Camera Capture Tool ===")
   print(f"Images will be saved to: {save_dir}")
   print("Controls:")
   print("  SPACE - Capture image")
   print("  ESC   - Exit")
   print("==========================")

   count = 0

   try:
      while True:
         # Capture frame
         frame = picam2.capture_array()

         # Display frame with instructions
         display = frame.copy()
         cv2.putText(display, f"Captured: {count} images", (10, 30),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
         cv2.putText(display, "Press SPACE to capture, ESC to exit", (10, 60),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

         cv2.imshow("Camera Capture", display)

         # Wait for key press
         key = cv2.waitKey(1) & 0xFF

         if key == 32:  # SPACE key
               # Save image
               filename = f"{save_dir}/img_{count:04d}.jpg"
               cv2.imwrite(filename, frame)
               print(f"Captured: {filename}")
               count += 1

               # Optional: flash effect
               flash = frame.copy()
               flash[:] = (255, 255, 255)
               cv2.imshow("Camera Capture", flash)
               cv2.waitKey(50)

         elif key == 27:  # ESC key
               print(f"\nExiting. Total captured: {count} images")
               break

   finally:
      cv2.destroyAllWindows()
      picam2.stop()
      print("Camera stopped")

**Transferir Imagenes a tu Ordenador**

Despues de capturar, usa :ref:`filezilla` para descargar las imagenes de la Raspberry Pi a tu ordenador:

1. Verifica la direccion IP en tu Raspberry Pi: ``hostname -I``
2. Conectate a la Raspberry Pi en FileZilla (usuario: pi, contrasena: tu contrasena)
3. Navega al directorio ``~/ai-lab-kit/yolo/captured_images/``
4. Descarga todas las imagenes a tu ordenador


----------------------------------------------------------


Entrenar el Modelo
-------------------------------------------------

Usaremos la plataforma en linea `Ultralytics Platform <https://platform.ultralytics.com/>`_. Esta plataforma proporciona servicios convenientes de entrenamiento de modelos sin necesidad de configurar entornos de entrenamiento complejos.

**Registro e Inicio de Sesion**

1. Haz clic en **Get started** en la esquina superior derecha para acceder a la pagina de registro y completar el proceso de registro.

.. image:: img/ultralytics_1_signup.png

**Crear un Conjunto de Datos**

2. Despues del registro, seras dirigido a la pagina de inicio. Haz clic en **New Dataset** para crear un nuevo conjunto de datos.

.. image:: img/ultralytics_3_new_dataset.png

3. Aparecera una ventana. Aqui puedes subir las fotos que acabas de capturar con tu Raspberry Pi e ingresar un **Nombre del conjunto de datos**. Luego haz clic en **Create & upload**.

.. image:: img/ultralytics_4_create_dataset.png

4. Ahora entraras en la interfaz del conjunto de datos, donde puedes ver todas las imagenes subidas.

.. image:: img/ultralytics_5_dataset.png

**Anotar Imagenes**

5. Abre cada foto para anotarla. Usa el boton **+Add Class** a la derecha para agregar categorias. Agrega el nombre de categoria apropiado segun el objeto que quieras identificar (por ejemplo: si entrenas para reconocer una taza, agrega "cup"; si entrenas para reconocer una mascota, agrega "pet").

   **Consejos de Anotacion**:
   - Usa el raton para dibujar cuadros delimitadores alrededor de los objetos, manteniendolos lo mas cerca posible de los bordes del objeto
   - Asegurate de que cada objeto este correctamente anotado
   - Si una imagen no contiene objetos objetivo, no es necesario anotarla

.. image:: img/ultralytics_6_train2.png

6. Repite los pasos anteriores hasta que todas las fotos esten anotadas. Verifica que las anotaciones en cada imagen sean precisas.

.. image:: img/ultralytics_7_train3.png

**Crear un Modelo de Entrenamiento**

7. Haz clic en **Models**, luego haz clic en **New Model**.

.. image:: img/ultralytics_8_new_model.png

8. En la ventana emergente, selecciona **YOLOv8n** o **YOLO11n** como **Modelo Base**. Estas son versiones nano adecuadas para Raspberry Pi, que ofrecen tamano pequeno y alta velocidad.

.. image:: img/ultralytics_9_new_model1.png

9. Configura los parametros de entrenamiento:

   - **Image size**: Selecciona **320** (este es el tamano de imagen que la Raspberry Pi puede procesar eficientemente)
   - **Epochs**: Manten el valor predeterminado (tipicamente 50-100 epochs)
   - **GPU Type**: No hay requisito especifico, pero diferentes tipos de GPU afectan la velocidad y el costo del entrenamiento

   **Nota**: Las nuevas cuentas de Ultralytics vienen con $5 en creditos gratuitos; entrenar un modelo pequeno tipicamente cuesta solo unos centavos, usa segun sea necesario.

.. image:: img/ultralytics_9_new_model2.png

10. Haz clic en **Start Training**. Espera un periodo (generalmente 10-30 minutos, dependiendo del volumen de datos y la GPU), y el modelo completara el entrenamiento.

    Durante el entrenamiento, puedes ver metricas en tiempo real:

    - **box_loss**: Perdida del cuadro delimitador; valores mas pequenos son mejores
    - **cls_loss**: Perdida de clasificacion; valores mas pequenos son mejores
    - **mAP**: Precision media promedio; valores mas altos son mejores (rango 0-1)

**Descargar e Implementar**

11. Despues de que el entrenamiento se complete, haz clic en **Download PyTorch Model** para descargar el modelo entrenado (sera un archivo .pt).

.. image:: img/ultralytics_10_download_model.png

12. Despues de descargar, usa FileZilla para transferirlo a tu Raspberry Pi (se recomienda colocarlo en el directorio ``~/ai-lab-kit/yolo/``).

**Ejecutar el Modelo Personalizado**

Despues de colocar el modelo en tu Raspberry Pi, necesitas modificar la ruta del modelo en el codigo de ejemplo. Aqui hay un ejemplo de ejecucion completo:

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   nano yolo_custom.py

reemplaza el nombre del archivo del modelo con tu propio archivo descargado:

.. code-block:: python
   :emphasize-lines: 6

   #!/usr/bin/env python3
   import cv2
   from picamera2 import Picamera2
   from ultralytics import YOLO

   model = YOLO("your_model.pt")  # Replace with your model filename

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

**Verificar Resultados**

13. Ejecuta el codigo de ejemplo para observar como se desempena el modelo YOLO en tu Raspberry Pi:

    .. code-block:: bash

       python3 yolo_custom.py

    Si todo funciona correctamente, deberias ver tu objeto objetivo entrenado enmarcado por un cuadro delimitador en el feed de la camara, con el nombre de la categoria y la puntuacion de confianza mostrados.

.. image:: img/ultralytics_a2_yolo_find.png


Felicidades! Has entrenado exitosamente tu propio modelo YOLO y lo has implementado en la Raspberry Pi.

----------------------------------------------------------

Consejos y Recomendaciones de Entrenamiento
-------------------------------------------------

**Mejorar el Rendimiento del Modelo**

* **Aumentar el Volumen de Datos**: Apunta a al menos 50-100 imagenes por categoria
* **Aumento de Datos**: Varía proactivamente los angulos, distancias e iluminacion durante la captura
* **Muestras Negativas**: Incluye algunas imagenes sin objetos objetivo para ayudar a reducir falsos positivos
* **Conjunto de Datos Equilibrado**: Si identificas multiples categorias, asegura cantidades de imagen similares para cada categoria



Preguntas Frecuentes
-------------------------


**P: ¿Que hago si los resultados de deteccion del modelo no son satisfactorios?**

- Verifica la precision de las anotaciones
- Aumenta el numero de imagenes de entrenamiento
- Prueba con modelos mas grandes (como YOLOv8s) o mas epochs de entrenamiento
- Captura mas imagenes de diferentes escenarios

**P: ¿Cuanto tiempo toma el entrenamiento?**

- Con aproximadamente 50 imagenes y YOLOv8n, el entrenamiento tipicamente toma 10-20 minutos
- La plataforma se ajusta automaticamente segun la GPU seleccionada

**P: ¿Puedo entrenar localmente?**

Si, pero necesitaras configurar el entorno Python y los controladores de GPU. Para principiantes, se recomienda la plataforma Ultralytics para validar ideas rapidamente.
