====================
 Total Open Station
====================

A program for downloading data from total station devices.

Introduction
============

I started writing this program for making it easier to manage different
models of total stations, often used in the same fieldwork unit, mainly in a
GNU/Linux environment. However, I try to develop following standards, so
porting to Windows or Mac shouldn't be difficult.

Every model has its own quirks. So, I decided to use a modular structure,
that is based on an abstract interface. Each time a new model is added to
the program, you create a new instance of this base class, with all needed
data.

This program is licensed under the GNU General Public License version 3.

The application icons are copyright by Lapo Calamandrei 2008.

GUI
===

The ``totalopenstation-gui.py`` module is a simple, yet complete user interface
for Total Open Station that allows to download, open and save raw data and export
into the available output formats.

CLI
===

The ``totalopenstation-cli-connector.py`` module is a command line user interface
to download and save raw data

Documentation
=============

Documentation is available at http://tops.berlios.de/docs/
with details on the application structure, supported models and other stuff.

