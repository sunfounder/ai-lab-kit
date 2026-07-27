.. include:: /index.rst
   :start-after: start_hello_message
   :end-before: end_hello_message


.. _assemble_hat:

.. start_assemble_hat

Montaje y Encendido del Fusion HAT+ (Importante)
=======================================================

Conectar Fusion HAT+ a Raspberry Pi
----------------------------------------

Aqui te ensenaremos como montar el Fusion HAT+.

#. Ensambla la base.
#. Pega la bateria a la base.
#. Asegura la Raspberry Pi con separadores.
#. Conecta el cable FPC a la Raspberry Pi. (Lo ensamblaremos junto con el modulo de la camara cuando montemos el pan-tilt).
#. Conecta el Fusion HAT+ al conector de 40 pines de la Raspberry Pi.
#. **Inserta la bateria.** (Esto es muy importante. Si no insertas la bateria, el Fusion HAT+ no funcionara.)


Para los detalles del montaje, consulta el video a continuacion.

.. raw:: html

  <iframe width="100%"
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/HlAayd1mSxU?si=oZnKyZihyyjQhsHl"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>



Carga
-------------------

Antes del primer uso, se recomienda cargar completamente la bateria. Puedes usar el cable de carga USB Type-C incluido o tu propio cargador USB-C.

.. note::

  La bateria puede llegar con poca carga porque Amazon requiere que este por debajo del 30% antes del transporte aereo. **DEBES** cargarla completamente antes de usarla para evitar una descarga excesiva y danos.
  Conecta el USB-C al Fusion HAT+ y la bateria se cargara automaticamente. No necesitas conectar la alimentacion a la Raspberry Pi.

* Recomendamos usar una **fuente de alimentacion de 5V 3A**, como el adaptador oficial de Raspberry Pi de 15W.
* Tambien puedes usar un cargador **USB-C PD (Power Delivery)** o un **cargador rapido QC 2.0**.
* La carga completa desde 0% normalmente toma aproximadamente **2 horas**.

.. image:: img/power_charge.jpg
   :width: 400
   :align: center

El Fusion HAT+ incluye **dos LED indicadores de bateria** que muestran el nivel de voltaje de la bateria:

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - Estado del LED
     - Voltaje de la Bateria
   * - 2 LED encendidos
     - > 7.4V
   * - 1 LED encendido
     - < 7.4V
   * - Ambos LED apagados
     - < 6.5V

Al cargar, uno de los LEDs parpadeara para indicar el progreso de la carga:

.. list-table::
   :header-rows: 1
   :widths: 40 40

   * - Estado del LED
     - Voltaje de la Bateria
   * - 1 LED encendido, 1 LED parpadeando
     - > 7.4V
   * - Solo 1 LED parpadeando
     - < 7.4V


Despues de la carga completa:

* **Si el Fusion HAT+ esta ENCENDIDO**, ambos LEDs permaneceran encendidos.
* **Si el Fusion HAT+ esta APAGADO**, ambos LEDs se apagaran.

.. note::

   Para sesiones prolongadas de programacion o depuracion, puedes mantener el Fusion HAT+ alimentado
   conectando el cable USB-C, lo que cargara la bateria y hara funcionar el Fusion HAT+ al mismo tiempo.
   Incluso si haces funcionar el Fusion HAT+ mientras el cargador esta conectado, la bateria **no** se puede extraer.

Encendido
----------------------

Cuando la bateria tenga carga suficiente, presiona brevemente el **boton de encendido** del Fusion HAT+.

* El **LED PWR** se encendera.
* Los **LED de bateria** tambien se encenderan.
* La Raspberry Pi se encendera automaticamente.

.. image:: img/power_button.jpg
    :width: 400

.. end_assemble_hat



.. _assemble_fusion_hat_pan_tilt:

Montaje del Pan-tilt (Para la Camara)
------------------------------------------------------

Para facilitar el uso del modulo de la camara, puedes ensamblar un pan-tilt.

.. note::

  El montaje del pan-tilt puede obstruir algunos pines, por lo que se recomienda ensamblarlo solo cuando se use la camara, o colocarlo en la parte exterior despues del montaje.


.. image:: img/gimbal_assemble.png

Para los detalles del montaje, consulta el video a continuacion.

.. raw:: html

  <iframe width="100%"
    style="aspect-ratio: 16/9; max-width: 100%;"
    src="https://www.youtube.com/embed/7CkGPKnbjM4"
    title="YouTube video player"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
    </iframe>
