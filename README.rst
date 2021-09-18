====================
 Total Open Station
====================


.. image:: https://travis-ci.com/totalopenstation/totalopenstation.svg?branch=master
  :target: https://travis-ci.com/totalopenstation/totalopenstation
  :alt: Travis

.. image:: https://img.shields.io/pypi/v/totalopenstation
  :target: https://pypi.org/project/totalopenstation/
  :alt: PyPI

.. image:: https://img.shields.io/readthedocs/totalopenstation
  :target: https://totalopenstation.readthedocs.io/
  :alt: Read the Docs

.. image:: https://img.shields.io/matrix/totalopenstation:matrix.org
   :target: https://matrix.to/#/#totalopenstation:matrix.org
   :alt: Matrix

|

Total Open Station is a program for downloading and processing survey data from total station devices.

.. image:: https://tops.iosa.it/img/totalopenstation-gui.gif

Total Open Station is a good choice if:

- you work with total stations on GNU/Linux (and MacOS, probably)
- you work with old devices that are unsupported by vendors
- you need to process hundreds of data files at once

We think Total Open Station is small but great because:

- it is *free/libre open source software*
- it works on *any* operating system where Python is available
- it is designed to support as many devices and formats as possible, all
  within the same program, opposed to having one program per device
- it works both on the command line and with a graphical interface

Total Open Station uses a modular structure and
keeps the downloading of data logically separated from its processing,
thus enabling exporting data to a variety of output formats, even at a
later moment. Archiving of raw data is made easy by using plain text
files.

Installing
==========

If you're comfortable with the command line:

.. code-block:: bash

    pip install totalopenstation

Windows users can download the portable app from the 
GitHub `releases page <https://github.com/steko/totalopenstation/releases>`_.

GNU/Linux users can find the `totalopenstation` package in some distributions
(OpenSUSE, Debian, Ubuntu). Make sure that `python3-tk` or `python3-tkinter` is
installed on your system, otherwise install it with your package manager (apt, dnf, pacman).

Documentation
=============

Documentation is online at http://totalopenstation.readthedocs.io/ with
an user guide, details on the application structure, supported models
and other interesting stuff.

Development
===========

Total Open Station is developed by @steko, @psolyca and other contributors, including
translators and providers of sample data. We are not professional software developers
but we do our best to follow modern good practice. Feel free to submit a feature request
or a pull request on GitHub.

The application icons are copyright by Lapo Calamandrei 2008, under the
same license as Total Open Station.
