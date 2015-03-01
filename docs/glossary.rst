.. _glossary:

Glossary
========

.. glossary::

   input format
      An input format is the way data downloaded from the total station
      are encoded. This might include a default order for X, Y and Z
      coordinates, particular ways of prefixing each point with some
      distinctive text string and other features. Each input format is
      unique, and it requires a dedicated module. Input formats are not
      readable by common CAD or GIS software packages, and it is TOPS's work
      to export them. These formats have a standard name, either given by the
      manufacturer or by the TOPS development team.

   model
      When we refer to a *model* we mean all total stations that
      have the same brand name and manufacturer (e.g. all those
      labeled “Trimble Geodimeter 600”).

   output format
      A format readable by GIS, CAD or any sort of common software,
      like CSV or DXF.

   serial-USB adapter
      While most total stations have a serial interface (port and cable),
      modern PCs and laptops tend to have just USB ports. In such cases, it
      is possible to use a serial-USB adapter cable, that enables you to
      connect the total station to one of your USB ports. Depending on your
      platform, the device might be identified as ``/dev/ttyUSB0`` or ``COM5``.
