.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Mostrar Imagen
==============================================

En este capítulo, exploraremos un ejemplo sencillo para ayudarte a experimentar rápidamente el uso básico de OpenCV: **leer y mostrar una imagen**.

En la carpeta del proyecto de ejemplo, ya hemos preparado una foto de muestra llamada ``my_photo.jpg``.
También puedes usar el ejemplo :ref:`py_photograph` para tomar una foto y guardarla en la carpeta actual.


1. Resumen del Proyecto
-----------------------

En esta sección, realizaremos las siguientes tareas:

- Usar ``cv2.imread`` para leer una imagen local
- Usar ``cv2.imshow`` para mostrar la imagen
- Usar ``cv2.waitKey`` para controlar el comportamiento de la ventana
- Usar ``cv2.destroyAllWindows`` para cerrar la ventana

Después de ejecutar este código correctamente, aparecerá una ventana con la imagen en tu pantalla.

.. image:: img/opencv_imshow.png
   :alt: Vista previa del resultado
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
      python3 cv_1_imgshow.py

#. Después de ejecutar el script, OpenCV abre una ventana titulada ``Picture`` y muestra la imagen cargada desde ``my_photo.jpg``.

   La ventana permanecerá abierta hasta que el usuario cierre el programa.

   Para salir del programa, puedes:

   * Presionar **q** en el teclado
   * Cerrar la ventana haciendo clic en el botón de cerrar

   Una vez que la ventana se cierra, todos los recursos de OpenCV se liberan y el programa finaliza.

3. Código Completo
-------------------

.. code-block:: python

   # Python code to read and display an image using OpenCV
   import cv2
   from pathlib import Path

   # Get the directory of the current Python file
   BASE_DIR = Path(__file__).resolve().parent

   # Read image from disk
   # cv2.imread loads the image as a NumPy array
   img = cv2.imread(str(BASE_DIR / "my_photo.jpg"), cv2.IMREAD_COLOR)

   # Create a GUI window to display the image
   # First parameter: window title
   # Second parameter: image array
   cv2.imshow("Picture", img)

   # Keep the window open until the user closes it or presses 'q'
   # cv2.waitKey only listens for keyboard events, not the close button
   # Therefore, we use a loop to detect both window close and key press
   while True:
      # Check if the window has been closed
      if cv2.getWindowProperty("Picture", cv2.WND_PROP_VISIBLE) < 1:
         break

      # Wait for 1 ms and check for key press
      # Press 'q' to exit the program
      if cv2.waitKey(1) & 0xFF == ord("q"):
         break

   # Destroy all OpenCV windows and release memory
   cv2.destroyAllWindows()

4. Explicación del Código
----------------------

- ``cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)``

  Lee la imagen llamada ``my_photo.jpg`` y la carga en modo color.

- ``cv2.imshow("Picture", img)``

  Crea una ventana titulada "Picture" y muestra la imagen.

- ``cv2.waitKey(0)``

  Cuando el parámetro es ``0``, el programa esperará indefinidamente hasta que cierres la ventana o presiones cualquier tecla.

- ``cv2.getWindowProperty()``

  Obtiene un valor de propiedad de la ventana especificada (por ejemplo, si la ventana sigue siendo visible).


- ``cv2.destroyAllWindows()``

  Cierra todas las ventanas de OpenCV y libera recursos.

5. Práctica Adicional
-----------------------

- Intenta cambiar el título de la ventana en ``imshow`` a "My First OpenCV Window".
- Reemplaza la imagen con una diferente y observa el resultado.
- Modifica el parámetro de ``waitKey`` a `3000` para que el programa cierre la ventana automáticamente después de 3 segundos.
