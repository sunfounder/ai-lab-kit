.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message

.. _faq:

FAQ
=====================


Vous trouverez ci-dessous quelques-unes des questions les plus frequentes que les utilisateurs peuvent rencontrer en utilisant le AI Fusion Lab Kit. Si votre probleme n'est pas liste ici, veuillez consulter les notes de depannage dans chaque chapitre ou contacter le support.

Questions generales
-------------------

**Ou puis-je telecharger l'image du systeme ?**

    Vous trouverez l'image recommandee du systeme Raspberry Pi ainsi que les instructions d'installation dans la section :ref:`get_start`. La documentation fournit egalement un guide d'installation pas a pas pour les debutants.

**Ai-je besoin d'une connexion Internet pour utiliser le kit ?**

    Les exemples Python de base et les exemples materiels ne necessitent pas de connexion Internet. Cependant, les LLM bases sur le cloud et certaines fonctionnalites d'IA necessitent une connexion Internet active.

**Quels modeles de Raspberry Pi sont pris en charge ?**

    Le kit supporte officiellement le Raspberry Pi 4B et le Raspberry Pi 5. D'autres modeles peuvent fonctionner mais ne sont pas garantis en raison de limitations de performances ou de compatibilite.

**Dois-je alimenter le FusionHAT separement ?**

    Oui. *Le FusionHAT necessite sa propre alimentation*. L'entree d'alimentation du Raspberry Pi ne fournit pas d'energie au FusionHAT. Si le FusionHAT n'est pas alimente, certaines fonctions — comme le haut-parleur ou d'autres modules integres — peuvent ne pas fonctionner correctement.

Logiciel / Installation
-----------------------

**RuntimeError: Failed to add edge detection / RuntimeError: Cannot determine SOC peripheral base address**

    Ce probleme est generalement cause par un conflit entre la bibliotheque ``RPi.GPIO`` installee par le systeme et la bibliotheque GPIO utilisee par Fusion HAT.
    Pour le resoudre, veuillez supprimer manuellement les fichiers du paquet systeme ``RPi.GPIO``, puis relancer le programme.

    1. Supprimez les fichiers systeme ``RPi.GPIO`` :

       .. code-block:: bash

          sudo pip3 uninstall RPi.GPIO --break
          sudo rm -rf /usr/lib/python3/dist-packages/RPi.GPIO*

    2. Redemarrez le Raspberry Pi :

       .. code-block:: bash

          sudo reboot

    3. Relancez l'exemple (n'utilisez pas sudo sauf si necessaire) :

Apres avoir supprime les fichiers ``RPi.GPIO`` conflictuels, l'exemple de bouton base sur les interruptions devrait fonctionner normalement.



**OSError: Fusion HAT not connected, check if Fusion Hat is powered on**

Si vous rencontrez cette erreur lors de l'execution de certains exemples (par exemple, lors de l'appel des broches PWM), les causes possibles sont :

1. Le Fusion HAT n'est pas correctement connecte ;
2. Une methode d'alimentation incorrecte ;
3. Le pilote du Fusion HAT est manquant apres une mise a jour du systeme Raspberry Pi.

Suivez les etapes ci-dessous pour verifier et resoudre le probleme :

1. Executez la commande suivante pour verifier l'etat du Fusion HAT :

   .. code-block:: bash

      i2cdetect -y 1

   Dans des conditions normales, vous devriez voir un resultat similaire a ce qui suit (avec ``UU`` a l'adresse ``0x1e``) :

   .. code-block:: bash

      pi@ai-fusion:~ $ i2cdetect -y 1
         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
      00:                         -- -- -- -- -- -- -- --
      10: -- -- -- -- -- -- -- UU -- -- -- -- -- -- -- --
      20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
      70: -- -- -- -- -- -- -- --

2. Si vous ne voyez pas ``UU`` mais ``17`` a la place, le pilote du Fusion HAT est manquant. Veuillez reinstaller le pilote en executant les commandes suivantes :

   .. code-block:: bash

      cd ~/fusion-hat/driver/
      make
      sudo make install

3. Si vous ne voyez ni ``UU`` ni ``17``, cela signifie que le Fusion HAT n'est pas connecte au Raspberry Pi ou qu'il y a un probleme d'alimentation. Veuillez vous assurer que votre Raspberry Pi est correctement connecte au Fusion HAT et que le Raspberry Pi est alimente par le Fusion HAT (et non de maniere independante).

4. Si les etapes ci-dessus ne resolvent pas le probleme, veuillez executer les commandes suivantes et nous envoyer le resultat :

   .. code-block:: bash

      uname -a
      cat /etc/os-release
      i2cdetect -y 1
      dmesg | grep fusion_hat
      lsmod | grep fusion_hat
      ls /sys/class/fusion_hat/fusion_hat
      cat ~/.ai-fusion

**Le script d'installation a echoue. Que dois-je faire ?**

    Assurez-vous que votre systeme Raspberry Pi OS est a jour et que vous disposez d'une connexion reseau stable pendant l'installation. Essayez de relancer le script d'installation. Si le probleme persiste, redemarrez le systeme et verifiez a nouveau votre version de Python.

**Les exemples Python ne peuvent pas s'executer. Quelle peut en etre la cause ?**

    Cela est generalement lie a des bibliotheques Python manquantes ou a une configuration d'environnement incorrecte. Verifiez que les dependances ont bien ete installees via le guide d'installation dans :ref:`get_start`.

**La camera n'est pas detectee.**

    Assurez-vous que le ruban de connexion est fermement branche et qu'il n'est pas insere a l'envers. Verifiez egalement que l'interface de la camera est activee dans les parametres de configuration du Raspberry Pi.

Fonctionnalites IA
------------------

**Les reponses du LLM sont lentes ou ne reviennent pas.**

    Cela indique souvent une mauvaise connectivite Internet ou des limites de taux d'API du fournisseur de modele selectionne. Essayez de changer de reseau ou de tester avec un modele different.

**La reconnaissance vocale (STT) est imprecise.**

    Verifiez la connexion de votre microphone et reduisez le bruit ambiant. Certains modeles peuvent necessiter des packs de langue supplementaires ou des ajustements de configuration.

**Message 'Error querying device -1' dans le module STT Vosk.**

    .. code-block:: bash

        stt = STT(language="en-us")
                ^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/stt/vosk.py", line 52, in __init__
            device_info = sd.query_devices(self._device, "input")
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/local/lib/python3.11/dist-packages/sounddevice.py", line 572, in query_devices
            raise PortAudioError(f'Error querying device {device}')
        sounddevice.PortAudioError: Error querying device -1

    Veuillez executer ``sudo /opt/setup_fusion_hat_audio.sh`` pour reconfigurer l'audio


**Permission denied lors de l'utilisation de TTS/STT**

    Lors de l'execution de commandes TTS (Text-to-Speech) ou STT (Speech-to-Text), vous rencontrez une erreur de permission comme :

    .. code-block:: bash

        Traceback (most recent call last):
            File "/home/pi/ai-lab-kit/llm/tts_piper.py", line 3, in <module>
                tts = Piper()
                    ^^^^^^^
            File "/usr/local/lib/python3.11/dist-packages/fusion_hat/tts.py", line 125, in _piper_init_with_speaker
                _original_piper_init(self, *args, **kwargs)
            File "/usr/local/lib/python3.11/dist-packages/sunfounder_voice_assistant/tts/piper.py", line 30, in __init__
                os.makedirs(PIPER_MODEL_DIR, 0o777)
            File "<frozen os>", line 225, in makedirs
        PermissionError: [Errno 13] Permission denied: '/opt/piper_models'


    Ce probleme se produit dans la version 0.0.1 du systeme d'exploitation AI Fusion Lab Kit. Le systeme tente de creer un repertoire (/opt/piper_models) qui necessite des privileges root, mais l'utilisateur actuel ne dispose pas des autorisations suffisantes. Mettez a jour le systeme d'exploitation AI Fusion Lab Kit de la version 0.0.1 vers 0.1.0 en executant la commande suivante :

    .. code-block:: bash

        curl -sSL https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/main/ai-fusion-lab-kit-upgrade-0.0.1-to-0.1.0.sh | sudo bash


Vision par ordinateur / MediaPipe
---------------------------------

**Les exemples OpenCV affichent des erreurs lors de l'acces a la camera.**

    Un seul processus peut acceder a la camera a la fois. Assurez-vous qu'aucune autre application camera ne fonctionne en arriere-plan.

**Les exemples MediaPipe s'executent lentement.**

    La vision par ordinateur en temps reel necessite une puissance de calcul importante. Pensez a reduire la resolution d'entree ou a fermer d'autres processus pour liberer des ressources systeme.

**Les projets MediaPipe ne fonctionnent pas sur la derniere version de Raspberry Pi OS.**

    MediaPipe ne supporte actuellement pas les dernieres versions du systeme Raspberry Pi (version Trixie) en raison de changements de dependances et d'architecture. Veuillez utiliser la version legacy (version Bookworm) qui prend en charge tous les exemples bases sur MediaPipe.

Problemes materiels
-------------------

**Un composant ne repond pas.**

    Revérifiez vos connexions de câblage et assurez-vous de l'orientation correcte. Reportez-vous a la section :ref:`cpn_list` pour les descriptions des broches et les schemas d'exemple.

**L'appareil cesse soudainement de fonctionner.**

    Cela peut etre cause par une instabilite de l'alimentation. Assurez-vous que votre alimentation repond aux specifications recommandées pour le modele de Raspberry Pi utilise.

Contact et support
------------------

**Comment puis-je obtenir de l'aide supplementaire ?**

    Vous pouvez consulter la documentation pour des etapes de depannage detaillees. Si vous avez des questions, n'hesitez pas a nous contacter a **service@sunfounder.com** — nous sommes la pour vous aider.
