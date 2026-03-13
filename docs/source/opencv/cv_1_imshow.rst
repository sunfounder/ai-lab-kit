.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Bild anzeigen
==============================================

In diesem Kapitel betrachten wir ein einfaches Beispiel, mit dem Sie schnell die grundlegende Verwendung von OpenCV kennenlernen: **Ein Bild lesen und anzeigen**.

Im Beispielprojektordner haben wir bereits ein Beispielbild mit dem Namen ``my_photo.jpg`` vorbereitet.  
Sie können auch das Beispiel :ref:`py_photograph` verwenden, um ein Foto aufzunehmen und im aktuellen Ordner zu speichern.


1. Projektübersicht
-------------------

In diesem Abschnitt führen wir folgende Aufgaben aus:

- Verwenden von ``cv2.imread``, um ein lokales Bild zu laden
- Verwenden von ``cv2.imshow``, um das Bild anzuzeigen
- Verwenden von ``cv2.waitKey``, um das Verhalten des Fensters zu steuern
- Verwenden von ``cv2.destroyAllWindows``, um das Fenster zu schließen

Nachdem dieser Code erfolgreich ausgeführt wurde, erscheint ein Bildfenster auf Ihrem Bildschirm.

.. image:: img/opencv_imshow.png
   :alt: Vorschau des Ergebnisses
   :align: center


2. Code ausführen
------------------------

.. important::

   Stellen Sie vor dem Start sicher, dass:

   * das Pan-Tilt-Modul montiert ist
   * Sie Zugriff auf den Raspberry-Pi-Desktop haben
   * das Codepaket installiert ist
   * das Fusion HAT+ installiert und konfiguriert ist
   * OpenCV installiert ist

   Detaillierte Anweisungen finden Sie unter :ref:`opencv_install`.


#. Öffnen Sie das Terminal und geben Sie den folgenden Befehl ein:

   .. code-block:: bash
   
      cd ~/ai-lab-kit/opencv_python
      python3 cv_1_imgshow.py

#. Nach dem Ausführen des Skripts öffnet OpenCV ein Fenster mit dem Titel ``Picture`` und zeigt das aus ``my_photo.jpg`` geladene Bild an.  

   Das Fenster bleibt geöffnet, bis der Benutzer das Programm beendet.
   
   Um das Programm zu beenden, können Sie:
   
   * **q** auf der Tastatur drücken  
   * das Fenster über die Schaltfläche zum Schließen schließen  
   
   Sobald das Fenster geschlossen wird, werden alle OpenCV-Ressourcen freigegeben und das Programm beendet.

3. Vollständiger Code
------------------------------

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

4. Code-Erklärung
----------------------

- ``cv2.imread("my_photo.jpg", cv2.IMREAD_COLOR)``  

  Liest das Bild mit dem Namen ``my_photo.jpg`` ein und lädt es im Farbmodus.

- ``cv2.imshow("Picture", img)``  

  Erstellt ein Fenster mit dem Titel „Picture“ und zeigt das Bild an.

- ``cv2.waitKey(0)``  

  Wenn der Parameter ``0`` ist, wartet das Programm unbegrenzt, bis Sie das Fenster schließen oder eine beliebige Taste drücken.

- ``cv2.getWindowProperty()``

  Ruft einen Eigenschaftswert des angegebenen Fensters ab (zum Beispiel, ob das Fenster noch sichtbar ist).


- ``cv2.destroyAllWindows()``  

  Schließt alle OpenCV-Fenster und gibt die Ressourcen frei.

5. Weitere Übungen
-----------------------

- Versuchen Sie, den Fenstertitel in ``imshow`` auf „My First OpenCV Window“ zu ändern.  
- Ersetzen Sie das Bild durch ein anderes und beobachten Sie das Ergebnis.  
- Ändern Sie den ``waitKey``-Parameter auf ``3000``, sodass das Programm das Fenster nach 3 Sekunden automatisch schließt.