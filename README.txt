====================
 Total Open Station
====================

A generic Python interface for downloading data from total station devices.

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

Helper application
==================

The helper application is found in the `helper` directory of the source tree.

To run it, you will need:

* the pySerial library
* the Python Tkinter GUI library

What the helper is
------------------

It is meant as a simple tool for obtaining two pieces of information:

1. the right **serial connection parameters** from an unknown device. The user
   can play with the 8 options and see the results in a text area. Once the
   downloaded results look good, we are almost sure that we have used the right
   parameters, and we can add the tested model to the program database.
2. **sample data dumps** from unknown models that are needed to develop new
   parser modules.

The helper consists of a single python module which can be executed stand-alone
on any platform. For Microsoft Windows, a single executable program is
available through `py2exe`. It has been reported to work on GNU/Linux
(including the OpenMoko FreeRunner) and Microsoft Windows.

What the helper is **not**
--------------------------

* The helper is not a beta version of Total Open Station
* The helper is not a draft of the final GUI
* The helper is not a broken Total Open Station implementation
* The helper is not ugly. It's just you who don't like Tk
* The helper is not a wizard. You have to tune the options using your prior
  knowledge of your total station.

Documentation
=============

Documentation is available at http://totalopenstation.sharesource.org/docs/
with details on the application structure, supported models and other stuff.

