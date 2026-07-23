.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

2. Détecter N'importe Quoi avec YOLOE
===========================================

YOLOE (You Only Look Once with Embeddings) est le dernier membre de la famille YOLO, introduisant des capacités d'apprentissage conjoint langage-vision au YOLO traditionnel. En termes simples, YOLOE peut non seulement détecter les objets sur lesquels il a été entraîné, mais aussi détecter de nouveaux objets arbitraires via des descriptions textuelles ou des indications sans réentraînement.

Principales caractéristiques de YOLOE :

* **Détection à vocabulaire ouvert** : Détectez des objets arbitraires via des descriptions textuelles, sans vous limiter à des catégories prédéfinies
* **Mode sans indication** : Détectez automatiquement les objets saillants dans les images sans aucune indication
* **Déploiement efficace** : Hérite de l'architecture efficace de YOLO, fonctionne de manière fluide sur Raspberry Pi
* **Support multi-tâches** : Prend en charge diverses tâches, y compris la détection d'objets et la segmentation d'instances

Cela rend YOLOE particulièrement adapté au prototypage rapide et aux applications nécessitant une détection flexible de divers objets.

Installation des Dépendances
---------------------------------------------------

Tout d'abord, installez la bibliothèque CLIP requise par YOLOE :

.. code-block:: bash

   pip3 install git+https://github.com/ultralytics/CLIP.git --break-system-packages

Mode Sans Indication
-----------------------------

Le mode sans indication est la manière la plus intuitive d'utiliser YOLOE. Dans ce mode, le modèle détecte automatiquement tous les objets saillants de l'image sans aucune indication textuelle. Cela se comporte de manière similaire au YOLO traditionnel mais avec de meilleures capacités de vocabulaire ouvert.

.. image:: img/yolo_prompt_free1.png

Figure : J'ai pointé la caméra vers mon bureau encombré, et le mode sans indication de YOLOE a automatiquement identifié et segmenté tous les objets saillants en vue — moniteur, clavier, gobelet d'eau, bloc-notes, souris... Chaque objet est annoté avec un masque de segmentation de couleur différente, sans nécessiter d'indications textuelles. Tout est présenté clairement en un coup d'œil.

**Comment ça fonctionne** : Le modèle identifie automatiquement les objets de premier plan dans l'image grâce à une analyse des caractéristiques visuelles et effectue la segmentation. Cette approche est adaptée pour parcourir rapidement le contenu d'une image ou lorsque vous ne savez pas quels objets doivent être détectés.

Le code suivant montre comment exécuter YOLOE en mode sans indication sur un Raspberry Pi :

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yoloe_prompt_free.py

.. code-block:: python

   from ultralytics import YOLO
   from picamera2 import Picamera2
   import cv2

   # prompt-free mode
   model = YOLO("yoloe-11s-seg-pf.pt")  # pf = prompt-free

   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("Prompt-free mode: detecting everything automatically...")
   print("Press 'q' to exit")

   while True:
      frame = picam2.capture_array()
      results = model.predict(frame, imgsz=320)
      annotated = results[0].plot()
      cv2.imshow("YOLOE Prompt-Free", annotated)

      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   cv2.destroyAllWindows()
   picam2.stop()

**Fonctionnalités du mode sans indication** :

* **Aucune configuration nécessaire** : Exécutez directement pour détecter les objets saillants dans les images
* **Segmentation automatique** : Produit à la fois des boîtes de détection et des masques de segmentation
* **Pas d'étiquettes de classe** : Affiche uniquement les emplacements des objets détectés sans noms de catégorie
* **Cas d'utilisation** : Parcours rapide, détection d'objets généraux, découverte d'objets inconnus

Mode d'Indication Textuelle
----------------------------------

Le mode d'indication textuelle est là où la puissance de YOLOE brille vraiment. Grâce à des descriptions en langage naturel, vous pouvez indiquer au modèle quels objets détecter, et le modèle identifiera et localisera ces objets en temps réel.

.. image:: img/yolo_prompt_word.png

Figure : J'ai tenu un morceau de papier moitié jaune moitié blanc devant la caméra, et j'ai utilisé une indication textuelle pour demander au modèle de chercher du « papier jaune ». YOLOE a compris précisément cette description, segmentant uniquement la moitié jaune du papier et la marquant d'une boîte englobante, tout en ignorant complètement la partie blanche. Cela démontre la capacité de YOLOE à effectuer une reconnaissance d'objets fine grâce au langage naturel.

**Comment ça fonctionne** : Le modèle encode les indications textuelles en vecteurs de caractéristiques, puis les compare aux caractéristiques de l'image pour identifier les régions qui correspondent le mieux aux descriptions textuelles. Cette approche vous permet de spécifier dynamiquement les cibles de détection sans réentraîner le modèle.

Le code suivant montre comment utiliser des indications textuelles pour détecter des objets spécifiques :

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   python3 yoloe_prompt_text.py

.. code-block:: python

   from ultralytics import YOLOE
   from picamera2 import Picamera2
   import cv2

   # load YOLOE model
   model = YOLOE("yoloe-26n-seg.pt")  # nano version

   # set the classes to detect (text prompt)
   names = ["yellow paper", "red cup", "person wearing glasses"]
   model.set_classes(names, model.get_text_pe(names))

   # initialize the camera
   picam2 = Picamera2()
   picam2.preview_configuration.main.size = (640, 480)
   picam2.preview_configuration.main.format = "RGB888"
   picam2.configure("preview")
   picam2.start()

   print("YOLOE running with text prompts, press 'q' to exit...")
   print(f"Detecting: {', '.join(names)}")

   while True:
      frame = picam2.capture_array()
      results = model.predict(frame, conf=0.3)  # set confidence threshold to 0.3
      annotated = results[0].plot()
      cv2.imshow("YOLOE on Raspberry Pi", annotated)

      if cv2.waitKey(1) & 0xFF == ord('q'):
         break

   cv2.destroyAllWindows()
   picam2.stop()

**Fonctionnalités du mode d'indication textuelle** :

* **Détection dynamique** : Modifiez les cibles de détection à tout moment sans réentraînement
* **Langage naturel** : Utilisez le langage courant pour décrire les objets, comme « voiture bleue », « chaise en bois »
* **Détection multi-cibles** : Spécifiez plusieurs cibles de détection à la fois
* **Contrôle fin** : Décrivez des attributs comme la couleur, le matériau, la forme, etc.
* **Seuil de confiance** : Contrôlez la sensibilité de la détection via le paramètre ``conf``

Utilisation Avancée
-------------------------------------

**Changement Dynamique des Cibles de Détection**

Vous pouvez modifier les indications textuelles pendant l'exécution sans redémarrer le programme :

.. code-block:: python

   # Initialize model
   model = YOLOE("yoloe-26n-seg.pt")

   # Initial detection targets
   current_names = ["red apple"]
   model.set_classes(current_names, model.get_text_pe(current_names))

   while True:
      frame = picam2.capture_array()

      # Check if detection target needs to be switched
      key = cv2.waitKey(1) & 0xFF
      if key == ord('1'):
         current_names = ["banana"]
         model.set_classes(current_names, model.get_text_pe(current_names))
         print("Now detecting: banana")
      elif key == ord('2'):
         current_names = ["orange"]
         model.set_classes(current_names, model.get_text_pe(current_names))
         print("Now detecting: orange")

      results = model.predict(frame, conf=0.3)
      annotated = results[0].plot()
      cv2.imshow("YOLOE", annotated)

      if key == ord('q'):
         break

**Utilisation de Descriptions Textuelles Plus Complexes**

YOLOE prend en charge des descriptions en langage naturel complexes pour une localisation d'objets plus précise :

.. code-block:: python

   # More precise description examples
   names = [
       "person wearing a red hat",
       "car with open door",
       "small dog on the left side",
       "yellow paper on the desk"
   ]
   model.set_classes(names, model.get_text_pe(names))

**Ajustement des Paramètres de Détection**

Optimisation des performances pour Raspberry Pi :

.. code-block:: python

   # Performance optimization configuration
   results = model.predict(
       frame,
       imgsz=224,        # Lower resolution for faster speed
       conf=0.4,         # Higher confidence threshold reduces false positives
       iou=0.5,          # Adjust IOU threshold
       verbose=False     # Disable verbose output
   )

Conseils d'Optimisation des Performances
-------------------------------------------------

Lors de l'exécution de YOLOE sur Raspberry Pi, les optimisations suivantes peuvent aider à obtenir de meilleures performances :

1. **Choisissez le bon modèle** :

   - ``yoloe-26n-seg.pt`` : Version nano, vitesse la plus rapide
   - ``yoloe-11s-seg-pf.pt`` : Version S, précision plus élevée mais plus lente

2. **Réduisez la résolution d'entrée** :

   - ``imgsz=224`` : Vitesse la plus rapide
   - ``imgsz=320`` : Choix équilibré (recommandé)
   - ``imgsz=416`` : Précision plus élevée

3. **Ajustez le seuil de confiance** :

   - L'augmentation du paramètre ``conf`` (par exemple, à 0,5) réduit le nombre de détections et améliore la vitesse

4. **Réduisez les catégories de détection** :

   - En mode d'indication textuelle, limiter la longueur de la liste ``names`` peut améliorer la vitesse d'inférence

FAQ
-------------------------

**Q : Quelle est la différence entre YOLOE et le YOLO traditionnel ?**

R : Le YOLO traditionnel ne peut détecter que les catégories fixes définies lors de l'entraînement, tandis que YOLOE peut détecter des objets arbitraires via des indications textuelles sans réentraînement.

**Q : Le mode sans indication détecte-t-il tous les objets ?**

R : Le mode sans indication détecte les objets visuellement saillants dans l'image mais ne fournit pas d'étiquettes de catégorie, ce qui le rend adapté pour parcourir rapidement les scènes.

**Q : L'indication textuelle supporte-t-elle le français ?**

R : Les indications en anglais sont recommandées pour de meilleurs résultats, car le modèle est principalement entraîné sur des données en anglais.

**Q : Quelle est la vitesse d'exécution de YOLOE sur Raspberry Pi ?**

R : Sur Raspberry Pi 5, en utilisant le modèle nano avec une résolution de 320, vous pouvez atteindre des performances en temps réel de 3 à 5 FPS.

**Q : Puis-je utiliser plusieurs indications textuelles simultanément ?**

R : Oui, ajoutez simplement plusieurs descriptions à la liste ``names``, et le modèle détectera tous ces objets simultanément.