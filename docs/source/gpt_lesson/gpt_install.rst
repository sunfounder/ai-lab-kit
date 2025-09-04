1.0 OpenAI Initial Configuration
==================================================

Dieses Kapitel führt Schritt für Schritt durch die Einrichtung der OpenAI-Entwicklungsumgebung auf einem Raspberry Pi.
Sie lernen, wie Sie ein OpenAI-Konto registrieren, den API-Schlüssel erhalten und die erforderlichen Python-Abhängigkeiten installieren.
Diese Schritte sind die Grundlage für den Aufbau von KI-Projekten wie GPT-Chatbots oder Spracherkennungs-Anwendungen.

**System Requirements**

* Betriebssystem: Raspberry Pi OS oder andere Debian-basierte Linux-Distributionen.
* Python-Version: 3.7 oder höher.
* Aktive Internetverbindung.


----------------------------------------------

Setting Up a Virtual Environment
------------------------------------------------


Um eine isolierte und gut wartbare Entwicklungsumgebung zu gewährleisten, erstellen und aktivieren wir eine virtuelle Umgebung.

Eine virtuelle Umgebung stellt für jedes Projekt eine unabhängige Python-Abhängigkeitsumgebung bereit. Das ist besonders bei komplexen Projekten wie GPT hilfreich, da es Konflikte zwischen Abhängigkeiten vermeidet und eine saubere, kontrollierte Entwicklungsbasis sicherstellt.

#. Erstellen Sie mit folgendem Befehl eine virtuelle Umgebung namens ``my_venv`` mit Zugriff auf systemweite Pakete. Die Option ``--system-site-packages`` erlaubt der virtuellen Umgebung, global installierte Pakete zu nutzen, z. B. vorinstallierte Gerätetreiber.

   .. code-block:: shell

      python -m venv --system-site-packages my_venv

#. Wechseln Sie in das Verzeichnis ``my_venv`` und aktivieren Sie die virtuelle Umgebung:

   .. code-block:: shell

      cd my_venv
      source bin/activate

.. note::

   Installieren Sie Abhängigkeiten stets *innerhalb* der virtuellen Umgebung und führen Sie Projekte dort aus.


----------------------------------------------

Installing Required Dependencies
-------------------------------------------

Sobald die virtuelle Umgebung aktiviert ist, installieren Sie die benötigten Python- und System-Abhängigkeiten.


#. Installieren Sie Python-Pakete innerhalb der virtuellen Umgebung:

   .. code-block:: shell

      pip3 install openai
      pip3 install openai-whisper
      pip3 install SpeechRecognition
      pip3 install -U sox
      pip3 install requests


#. Installieren Sie systemweite Abhängigkeiten über den Paketmanager ``apt`` mit Administratorrechten:

   .. code-block:: shell

      sudo apt install python3-pyaudio
      sudo apt install sox

----------------------------------------------

Obtaining an API Key
-----------------------------------------

Die OpenAI-API bietet eine einfache Schnittstelle zu fortgeschrittenen KI-Modellen für Natural Language Processing,
Bildgenerierung, semantische Suche und Spracherkennung.

**Get API Key**

.. note::

   Der API-Schlüssel ist Ihr eindeutiger Identifikator für den Zugriff auf OpenAI-Dienste. Bewahren Sie ihn sicher auf und geben Sie ihn nicht öffentlich weiter.


#. Besuchen Sie |link_openai_platform| und klicken Sie oben rechts auf **Create new secret key**.

   .. image:: img/apt_create_api_key.png
      :width: 700
      :align: center

#. Wählen Sie bei Bedarf Owner, Name, Project und Berechtigungen aus und klicken Sie anschließend auf **Create secret key**.

   .. image:: img/apt_create_api_key2.png
      :width: 700
      :align: center

#. Speichern Sie den generierten Schlüssel an einem sicheren, zugänglichen Ort. **You will not be able to view it again** in Ihrem OpenAI-Konto. Geht der Schlüssel verloren, müssen Sie einen neuen erstellen.

   .. image:: img/apt_create_api_key_copy.png
      :width: 700
      :align: center

.. note::
   * Jeder Schlüssel hat Nutzungs- und Ratenlimits. Weisen Sie Schlüssel bedarfsgerecht zu.
   * Vermeiden Sie das Hardcodieren des Schlüssels in Skripten; nutzen Sie stattdessen Umgebungsvariablen für höhere Sicherheit.



**Fill in API Key and Assistant ID**

#. Öffnen Sie die Datei ``keys.py`` mit folgendem Befehl:

   .. code-block:: shell

      nano ~/ai-explorer-lab-kit/gpt_example/keys.py

#. Fügen Sie den kopierten API-Schlüssel ein:

   .. code-block:: shell

      OPENAI_API_KEY = "sk-proj-vEBo7Ahxxxx-xxxxx-xxxx"

#. Drücken Sie ``Ctrl + X``, ``Y`` und anschließend ``Enter``, um die Datei zu speichern und den Editor zu verlassen.

.. ----------------------------------------------

.. Setting Permissions
.. -----------------------------------------------------

.. Certain examples may require elevated permissions to run successfully within the virtual environment. 
.. Execute the following command to ensure proper permissions:

.. .. code-block:: shell

..    cd ~/ai-explorer-lab-kit/gpt_example
..    chmod 755 

.. 
   .. warning::
..    Avoid using ``chmod 777`` unless absolutely necessary, as it grants full permissions to all users, which can pose a security risk. Use ``chmod 755`` to grant sufficient permissions while maintaining security.