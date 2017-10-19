.. TotalOpenStation documentation master file, created by
   sphinx-quickstart on Sat May 24 15:43:10 2008.  You can adapt this
   file completely to your liking, but it should at least contain the
   root `toctree` directive.

==================
Total Open Station
==================

Total Open Station (TOPS for friends) is a free software program for
downloading and processing data from total station devices.

This is a task which is usually done by proprietary, dedicated and
Windows™-only software, but TOPS is different by nature, because:

- it is **free software** released under the GNU GPLv3 license;
- it works on *any* operating system, including mobile platforms like
  OpenMoko;
- it is designed to support as many devices and formats as possible, all
  within the same program, opposed to having one program per device.

Every model has its own quirks, but TOPS uses a modular structure and
keeps the downloading of data logically separated from its processing,
thus enabling exporting data to a variety of output formats, even at a
later moment. Archiving of raw data is made easy by using plain text
files.

:ref:`users` are a growing number, you can be the next. See which
:ref:`models` are already supported.

Getting started with Total Open Station
=======================================

Total Open Station 0.3 is in now available as a development preview and
can be installed on all major operating systems.

Detailed instructions are available at the :ref:`installing` page.

If you are having problems with getting started, try first our
:ref:`faq`. If that doesn't help, get in touch with the development
team through our dedicated support channel and `mailing list`_.

.. _`mailing list`: https://lists.berlios.de/mailman/listinfo/tops-dev

Documentation
=============


User manual
-----------

.. toctree::
   :maxdepth: 1
   :glob:

   installing
   interfaces/main
   input_formats/main
   models/main
   glossary
   library
   faq

.. toctree::
   :hidden:

   interfaces/cli_connector
   interfaces/cli_parser
   interfaces/gui_main

Development
-----------

.. toctree::
   :maxdepth: 1
   :glob:

   contributing
   users
   release

.. toctree::
   :hidden:

   input_formats/new

Indices and tables
------------------

* :ref:`genindex`
* :ref:`Implemented Formats <implemented_formats>`
* :ref:`Implemented Models <implemented_models>`
* :ref:`modindex`
* :ref:`search`


Who is doing this?
==================

Total Open Station is mainly developed as part of the IOSA_ project by
Stefano Costa and Luca Bianconi, archaeologists.

.. _IOSA: http://www.iosa.it/

Damien Gaignon, land surveyor, has joined the project in september 2015.

Total Open Station is licensed under the GNU General Public License
version 3 or, at your option, any later version.

The application icons are copyright by Lapo Calamandrei 2008.
