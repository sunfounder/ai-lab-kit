.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

3. Entraîner Votre Propre Modèle YOLO
==========================================

Entraîner votre propre modèle YOLO consiste essentiellement à laisser l'algorithme d'apprentissage profond apprendre à identifier des objets spécifiques à partir des données d'image que vous fournissez. Ce processus peut être comparé à l'apprentissage d'un enfant à reconnaître quelque chose de nouveau : vous lui montrez de nombreux exemples d'images sous différents angles et environnements, en lui disant « c'est l'objet cible ». Après suffisamment d'exemples, il peut identifier précisément cet objet dans de nouvelles images.

Pour YOLO, le processus d'entraînement fonctionne comme suit :

1. **Préparation des données** : Collectez des images contenant les objets cibles et annotez la position et la catégorie de chaque objet
2. **Apprentissage du modèle** : L'algorithme apprend automatiquement les schémas caractéristiques des objets en analysant ces données annotées
3. **Génération des poids** : Après l'entraînement, générez un fichier de modèle (fichier .pt) contenant les connaissances apprises
4. **Application d'inférence** : Déployez ce modèle sur le Raspberry Pi pour la détection sur de nouvelles images

Grâce à l'apprentissage par transfert, nous n'avons pas besoin d'entraîner à partir de zéro. La plateforme Ultralytics fournit des modèles de base pré-entraînés (comme YOLOv8n) qui ont été entraînés sur des millions d'images. Nous n'avons besoin que de « fine-tuner » ces modèles avec un petit nombre de nos propres images pour créer des modèles personnalisés efficaces.



----------------------------------------------------------

Prise de Photos
--------------

Puisque notre projet YOLO est basé sur le Raspberry Pi, nous utiliserons la caméra Raspberry Pi pour prendre des photos. Pour de meilleurs résultats, nous avons également utilisé des téléphones portables pour prendre quelques photos afin d'augmenter la diversité des données.

**Conseils pour la prise de photos**

* **Clarté** : Capturez les objets aussi clairement que possible, en évitant le flou
* **Diversité** : Prenez des photos sous différents angles (face, côté, dessus, etc.) et dans différentes conditions d'éclairage (lumière vive, faible luminosité, contre-jour, etc.)
* **Variation d'arrière-plan** : Essayez de prendre des images avec différents arrière-plans pour aider le modèle à apprendre les caractéristiques essentielles des objets plutôt que des arrière-plans
* **Évitez les chevauchements** : Vous pouvez capturer plusieurs objets simultanément, mais évitez les chevauchements importants entre les objets
* **Quantité recommandée** : Visez au moins 50 à 100 photos par catégorie ; plus d'images donnent de meilleurs résultats

**Quel objet devriez-vous utiliser ?**

Vous pouvez choisir n'importe quel objet qui vous intéresse pour l'entraînement, comme : une poupée, une tasse, une chaise, ou même votre animal de compagnie. Ce tutoriel utilise un bonhomme de neige jouet comme exemple ; remplacez-le simplement par votre propre objet cible.

.. image:: img/ultralytics_a1_capture_photo.png

**Prise de photos avec la caméra Raspberry Pi**

Voici le code pour prendre des photos en utilisant la caméra Raspberry Pi :

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

**Transférer les images vers votre ordinateur**

Après la capture, utilisez :ref:`filezilla` pour télécharger les images du Raspberry Pi vers votre ordinateur :

1. Vérifiez l'adresse IP sur votre Raspberry Pi : ``hostname -I``
2. Connectez-vous au Raspberry Pi dans FileZilla (utilisateur : pi, mot de passe : votre mot de passe)
3. Naviguez vers le répertoire ``~/ai-lab-kit/yolo/captured_images/``
4. Téléchargez toutes les images vers votre ordinateur


----------------------------------------------------------


Entraînement du Modèle
-------------------------------------------------

Nous utiliserons la `plateforme Ultralytics <https://platform.ultralytics.com/>`_ en ligne. Cette plateforme fournit des services d'entraînement de modèles pratiques sans avoir à configurer des environnements d'entraînement complexes.

**Inscription et Connexion**

1. Cliquez sur **Get started** dans le coin supérieur droit pour accéder à la page d'inscription et terminer le processus d'inscription.

.. image:: img/ultralytics_1_signup.png

**Création d'un Ensemble de Données**

2. Après l'inscription, vous serez redirigé vers la page d'accueil. Cliquez sur **New Dataset** pour créer un nouvel ensemble de données.

.. image:: img/ultralytics_3_new_dataset.png

3. Une fenêtre s'affiche. Vous pouvez y télécharger les photos que vous venez de prendre avec votre Raspberry Pi et saisir un **nom d'ensemble de données**. Cliquez ensuite sur **Create & upload**.

.. image:: img/ultralytics_4_create_dataset.png

4. Vous entrez maintenant dans l'interface de l'ensemble de données, où vous pouvez voir toutes les images téléchargées.

.. image:: img/ultralytics_5_dataset.png

**Annotation des Images**

5. Ouvrez chaque photo pour l'annoter. Utilisez le bouton **+Add Class** à droite pour ajouter des catégories. Ajoutez le nom de catégorie approprié en fonction de l'objet que vous souhaitez identifier (par exemple : si vous vous entraînez à reconnaître une tasse, ajoutez « cup » ; si vous vous entraînez à reconnaître un animal de compagnie, ajoutez « pet »).

   **Conseils d'annotation** :
   - Utilisez la souris pour dessiner des boîtes englobantes autour des objets, en les gardant aussi proches que possible des bords de l'objet
   - Assurez-vous que chaque objet est correctement annoté
   - Si une image ne contient pas d'objets cibles, aucune annotation n'est nécessaire

.. image:: img/ultralytics_6_train2.png

6. Répétez les étapes ci-dessus jusqu'à ce que toutes les photos soient annotées. Vérifiez que les annotations sur chaque image sont précises.

.. image:: img/ultralytics_7_train3.png

**Création d'un Modèle d'Entraînement**

7. Cliquez sur **Models**, puis cliquez sur **New Model**.

.. image:: img/ultralytics_8_new_model.png

8. Dans la fenêtre contextuelle, sélectionnez **YOLOv8n** ou **YOLO11n** comme **modèle de base**. Ce sont des versions nano adaptées au Raspberry Pi, offrant une petite taille et une grande rapidité.

.. image:: img/ultralytics_9_new_model1.png

9. Configurez les paramètres d'entraînement :

   - **Image size** : Sélectionnez **320** (c'est la taille d'image que le Raspberry Pi peut traiter efficacement)
   - **Epochs** : Conservez la valeur par défaut (généralement 50 à 100 époques)
   - **GPU Type** : Aucune exigence particulière, mais différents types de GPU affectent la vitesse et le coût d'entraînement

   **Remarque** : Les nouveaux comptes Ultralytics bénéficient de 5 $ de crédits gratuits ; l'entraînement d'un petit modèle ne coûte généralement que quelques centimes, utilisez selon vos besoins.

.. image:: img/ultralytics_9_new_model2.png

10. Cliquez sur **Start Training**. Attendez un certain temps (généralement 10 à 30 minutes, selon le volume de données et le GPU), et le modèle terminera l'entraînement.

    Pendant l'entraînement, vous pouvez voir des métriques en temps réel :

    - **box_loss** : Perte de la boîte englobante ; des valeurs plus petites sont meilleures
    - **cls_loss** : Perte de classification ; des valeurs plus petites sont meilleures
    - **mAP** : Précision moyenne moyenne ; des valeurs plus élevées sont meilleures (plage 0-1)

**Téléchargement et Déploiement**

11. Une fois l'entraînement terminé, cliquez sur **Download PyTorch Model** pour télécharger le modèle entraîné (ce sera un fichier .pt).

.. image:: img/ultralytics_10_download_model.png

12. Après le téléchargement, utilisez FileZilla pour le transférer vers votre Raspberry Pi (recommandé de le placer dans le répertoire ``~/ai-lab-kit/yolo/``).

**Exécution du Modèle Personnalisé**

Après avoir placé le modèle sur votre Raspberry Pi, vous devez modifier le chemin du modèle dans le code d'exemple. Voici un exemple d'exécution complet

.. code-block:: bash

   cd ~/ai-lab-kit/yolo
   nano yolo_custom.py

remplacez le nom du fichier de modèle par votre propre fichier téléchargé :

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

**Vérification des Résultats**

13. Exécutez le code d'exemple pour observer comment le modèle YOLO fonctionne sur votre Raspberry Pi :

    .. code-block:: bash

       python3 yolo_custom.py

    Si tout fonctionne correctement, vous devriez voir votre objet cible entraîné encadré par une boîte englobante dans le flux de la caméra, avec le nom de la catégorie et le score de confiance affichés.

.. image:: img/ultralytics_a2_yolo_find.png


Félicitations ! Vous avez réussi à entraîner votre propre modèle YOLO et à le déployer sur le Raspberry Pi.

----------------------------------------------------------

Conseils et Recommandations pour l'Entraînement
-------------------------------------------------

**Amélioration des Performances du Modèle**

* **Augmentez le volume de données** : Visez au moins 50 à 100 images par catégorie
* **Augmentation des données** : Variez proactivement les angles, les distances et l'éclairage lors de la capture
* **Échantillons négatifs** : Incluez quelques images sans objets cibles pour aider à réduire les faux positifs
* **Ensemble de données équilibré** : Si vous identifiez plusieurs catégories, assurez-vous d'avoir un nombre d'images similaire pour chaque catégorie



Questions Courantes
-------------------------


**Q : Que faire si les résultats de détection du modèle ne sont pas satisfaisants ?**

- Vérifiez la précision des annotations
- Augmentez le nombre d'images d'entraînement
- Essayez des modèles plus grands (comme YOLOv8s) ou plus d'époques d'entraînement
- Capturez plus d'images dans différents scénarios

**Q : Combien de temps prend l'entraînement ?**

- Avec environ 50 images et YOLOv8n, l'entraînement prend généralement 10 à 20 minutes
- La plateforme s'ajuste automatiquement en fonction du GPU sélectionné

**Q : Puis-je entraîner localement ?**

Oui, mais vous devrez configurer l'environnement Python et les pilotes GPU. Pour les débutants, la plateforme Ultralytics est recommandée pour valider rapidement les idées.