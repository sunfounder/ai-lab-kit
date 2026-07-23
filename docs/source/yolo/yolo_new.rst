.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

1. Exécuter YOLO sur Raspberry Pi
==================================================================

YOLO (You Only Look Once) est un algorithme de détection d'objets révolutionnaire caractérisé par sa vitesse et sa précision. Il transforme la détection d'objets en un problème de régression, prédisant toutes les catégories et positions d'objets dans une image en un seul passage direct du réseau neuronal.

Considérez-le comme un système de vision capable de « tout voir d'un seul coup d'œil ». Qu'il s'agisse de surveillance vidéo, de conduite autonome ou d'inspection qualité industrielle, YOLO est présent partout où une détection d'objets en temps réel est nécessaire.

.. image:: img/yolo_new.png

Figure : YOLOv8n fonctionnant en temps réel sur Raspberry Pi. Les objets dans le flux de la caméra sont détectés et annotés avec précision, les classes détectées et les scores de confiance étant affichés à gauche. Cette image montre le modèle identifiant avec succès des objets tels qu'une personne, une chaise et une télévision.

Principes Fondamentaux
------------------------------------------

Contrairement aux méthodes antérieures en deux étapes (comme R-CNN) qui « trouvent d'abord les régions candidates puis les identifient », YOLO adopte une approche fondamentalement différente :

* **Cadre Unifié** : Divise l'image en une grille (par exemple, la grille 7x7 d'origine).

* **Prédiction par Grille** : Chaque cellule de la grille est responsable de la prédiction des objets dont le centre tombe dans cette cellule. Chaque cellule prédit plusieurs boîtes englobantes (incluant la position et la taille) avec leurs scores de confiance, tout en prédisant les probabilités des classes d'objets.

* **Réalisation en Une Étape** : La classification et la localisation sont accomplies simultanément dans le même réseau neuronal, réalisant véritablement « you only look once », surpassant ainsi significativement les méthodes précédentes en vitesse.


Exécution du Code
------------------------------------

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yolo_test.py

Le code téléchargera automatiquement un modèle (environ 6 Mo) et l'exécutera sur la caméra. Les résultats seront affichés dans une fenêtre intitulée « YOLOv8 ».

(la première exécution téléchargera automatiquement un modèle d'environ 6 Mo) :

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



Dépannage
---------------

Q : Si vous rencontrez une erreur Numpy.dtype size changed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Abaissez la version de Numpy :

.. code-block:: bash

   # If version is 2.x, downgrade to 1.x
   pip3 install "numpy<2.0" --break-system-packages --force-reinstall

Q : Si vous rencontrez une erreur ``libopenblas.so.0`` manquant
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installez la bibliothèque OpenBLAS :

.. code-block:: bash

   sudo apt install libopenblas-dev

Q : Si la caméra ne peut pas être ouverte
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vérifiez la connexion de la caméra et assurez-vous qu'elle est activée :

.. code-block:: bash

   sudo raspi-config
   # Select Interface Options -> Camera -> Enable

Q : Si vous rencontrez des erreurs de mémoire insuffisante
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Augmentez l'espace d'échange :

.. code-block:: bash

   sudo dphys-swapfile swapoff
   sudo nano /etc/dphys-swapfile
   # Modify CONF_SWAPSIZE=2048
   sudo dphys-swapfile setup
   sudo dphys-swapfile swapon

Méthodes d'Optimisation des Performances
--------------------------------------------------------

Exécuter YOLO sur un Raspberry Pi (même 4B/5) peut être exigeant. Voici plusieurs méthodes d'optimisation éprouvées :

1. **Ajuster la résolution d'inférence YOLO** : Le code ci-dessus utilise déjà imgsz=320, ce qui est un réglage équilibré. Valeurs ajustables :

   * ``imgsz=224`` - Résolution la plus basse, vitesse la plus rapide
   * ``imgsz=320`` - Choix standard
   * ``imgsz=416`` - Précision plus élevée, vitesse plus lente
   * ``imgsz=640`` - Précision la plus élevée, très lent sur Raspberry Pi

2. **Choisir le bon modèle** :

   * ``yolov8n.pt`` (6 Mo) - Le plus rapide, adapté à la détection en temps réel
   * ``yolov8s.pt`` (22 Mo) - Légèrement plus lent mais plus précis
   * ``yolov8m.pt`` (49 Mo) - Plus lent, précision plus élevée
   * ``yolov8l/x.pt`` - Généralement inutilisable sur Raspberry Pi
   * Vous pouvez également utiliser votre propre modèle entraîné, par exemple ``"/home/pi/my_model.pt"``. Nous verrons comment entraîner des modèles personnalisés dans les chapitres suivants.

3. **Limiter les classes de détection** : Si vous ne détectez que des objets spécifiques (par exemple, uniquement les personnes), modifiez le code :

.. code-block:: python

   results = model(frame, classes=[0], imgsz=320)  # 0 is the class ID for person

Identifiants de classe courants :

   * 0 - personne
   * 1 - vélo
   * 2 - voiture
   * 3 - moto
   * 5 - bus
   * 7 - camion

4. **Utiliser des variantes de modèles légers** :

.. code-block:: python

   # Use pruned version of YOLOv8n (if available)
   model = YOLO("yolov8n.pt")

   # Or use TensorRT acceleration (requires additional configuration)
   # model = YOLO("yolov8n.pt")
   # model.export(format="engine")  # Export as TensorRT engine

5. **Réduire le traitement des images** : Si l'affichage en temps réel de toutes les images n'est pas nécessaire, traitez les images de manière intermittente :

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

6. **Utiliser le multithreading** : Séparez la capture de la caméra et l'inférence YOLO dans différents threads :

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

Utilisation Avancée
--------------------------------

Utilisation de Fichiers Vidéo comme Entrée
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Résumé
------------------

Grâce à ce tutoriel, vous avez appris :

* Comment configurer l'environnement YOLO sur Raspberry Pi
* Comment effectuer une détection d'objets en temps réel à l'aide de la caméra
* Comment résoudre les problèmes d'installation et d'exécution courants
* Diverses méthodes pour optimiser les performances de détection

La puissance de YOLO réside dans sa simplicité et son efficacité, permettant d'obtenir des performances de détection d'objets respectables même sur des appareils embarqués comme le Raspberry Pi. Continuez à explorer et vous pourrez construire diverses applications intéressantes telles que la surveillance intelligente, le suivi d'objets et le comptage de personnes.