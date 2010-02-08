====================
 Total Open Station
====================

Total Open Station (TOPS for friends) is a free software program for
downloading and processing data from total station devices, written in
the Python programming language.

This is a task which is usually done by proprietary, dedicated and
Windows™-only software, but TOPS is different by nature, because:

- it is *free software* released under the GNU GPLv3 license;
- it works on *any* operating system, including mobile platforms like
  OpenMoko;
- it is designed to support as many devices and formats as possible, all
  within the same program, opposed to having one program per device.

Every model has its own quirks, but TOPS uses a modular structure and
keeps the downloading of data logically separated from its processing,
thus enabling exporting data to a variety of output formats, even at a
later moment. Archiving of raw data is made easy by using plain text
files.

The application icons are copyright by Lapo Calamandrei 2008.

GUI
===

The ``totalopenstation-gui`` module is a simple, yet complete
graphical user interface for Total Open Station that allows to
download, open and save raw data and export into the available output
formats. It is currently based on Tkinter and works on all major
platforms (tested on GNU/Linux and Microsoft Windows).

CLI
===

The ``totalopenstation-cli-connector`` module is a command line
user interface to download and save raw data, while its companion
``totalopenstation-cli-parser`` is responsible for parsing and
exporting data.

Documentation
=============

Documentation is available at in the ``docs`` subdirectory of this
package and online at http://tops.berlios.de/ with an user guide,
details on the application structure, supported models and other
stuff.
