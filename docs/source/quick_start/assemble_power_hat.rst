.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _assemble_hat:

.. start_assemble_hat

Assembler et alimenter le Fusion HAT+ (Important)
=======================================================

Connecter le Fusion HAT+ au Raspberry Pi
-----------------------------------------

Nous allons vous montrer comment assembler le Fusion HAT+.

#. Assemblez le socle.
#. Fixez la batterie au socle.
#. Fixez le Raspberry Pi a l'aide d'entretoises.
#. Connectez le cable FPC au Raspberry Pi. (Nous l'assemblerons ainsi que le module camera lors du montage du pied panoramique.)
#. Branchez le Fusion HAT+ sur le connecteur 40 broches du Raspberry Pi.
#. **Inserez la batterie.** (Ceci est tres important. Si vous n'inserez pas la batterie, le Fusion HAT+ ne fonctionnera pas.)


Pour les details de l'assemblage, veuillez regarder la video ci-dessous.

.. raw:: html

  <iframe width="100%"
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/HlAayd1mSxU?si=oZnKyZihyyjQhsHl"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>



Charger
-------------------

Avant la premiere utilisation, il est recommande de charger completement la batterie. Vous pouvez utiliser le cable de charge USB Type-C inclus, ou votre propre chargeur USB-C.

.. note::

  La batterie peut arriver avec une charge faible car Amazon exige qu'elle soit inferieure a 30% avant le transport aerien. Vous **DEVEZ** la charger completement avant utilisation pour eviter une decharge excessive et des dommages.
  Branchez le cable USB-C sur le Fusion HAT+ et la batterie se chargera automatiquement. Vous n'avez pas besoin de connecter l'alimentation au Raspberry Pi.

* Nous recommandons d'utiliser une **alimentation 5V 3A**, comme l'adaptateur officiel Raspberry Pi 15W.
* Vous pouvez egalement utiliser un chargeur **USB-C PD (Power Delivery)** ou un chargeur rapide **QC 2.0**.
* La charge de 0% a pleine capacite prend generalement environ **2 heures**.

.. image:: img/power_charge.jpg
   :width: 400
   :align: center

Le Fusion HAT+ est equipe de **deux LED d'indication de batterie**, indiquant le niveau de tension de la batterie :

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - Etat des LED
     - Tension de la batterie
   * - 2 LED ALLUMEES
     - > 7,4 V
   * - 1 LED ALLUMEE
     - < 7,4 V
   * - Les deux LED ETEINTES
     - < 6,5 V

Lors de la charge, l'une des LED clignote pour indiquer la progression de la charge :

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - Etat des LED
     - Tension de la batterie
   * - 1 LED ALLUMEE, 1 LED Clignotante
     - > 7,4 V
   * - Seulement 1 LED Clignotante
     - < 7,4 V


Apres une charge complete :

* **Si le Fusion HAT+ est ALLUME**, les deux LED restent allumees.
* **Si le Fusion HAT+ est ETEINT**, les deux LED s'eteignent.

.. note::

   Pour des sessions de programmation ou de debogage prolongees, vous pouvez maintenir le Fusion HAT+ alimente
   en branchant le cable USB-C, ce qui chargera la batterie et fera fonctionner le Fusion HAT+ en meme temps.
   Meme si vous faites fonctionner le Fusion HAT+ alors que le chargeur est branche, la batterie **ne peut pas** etre retiree.

Mettre sous tension
----------------------

Lorsque la batterie est suffisamment chargee, appuyez brievement sur le **bouton d'alimentation** du Fusion HAT+.

* La **LED PWR** s'allume.
* Les **LED de batterie** s'allument egalement.
* Le Raspberry Pi se met sous tension automatiquement.

.. image:: img/power_button.jpg
    :width: 400

.. end_assemble_hat



.. _assemble_fusion_hat_pan_tilt:

Assembler le pied panoramique (Pour la camera)
------------------------------------------------------

Pour faciliter l'utilisation du module camera, vous pouvez assembler un pied panoramique.

.. note::

  L'assemblage du pied panoramique peut masquer certaines broches, il est donc recommande de ne l'assembler que lors de l'utilisation de la camera, ou de le placer a l'exterieur apres l'assemblage.


.. image:: img/gimbal_assemble.png

Pour les details de l'assemblage, veuillez regarder la video ci-dessous.

.. raw:: html

  <iframe width="100%"
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/7CkGPKnbjM4"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>
