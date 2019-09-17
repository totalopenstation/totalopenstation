.. _installing:

=============================
Installing Total Open Station
=============================

There are a few different ways to install Total Open Station,
depending on your operating system.

.. warning::

    Version 0.4.0 of Total Open Station is the last version built on Python2. |br|
    **Thus no support will be done on this version after 0.5 release as Python2 has reached his EOL.** |br|
    Version 0.5+ will be Python3 only. |br|

GNU/Linux distributions
=======================

OpenSUSE
--------

Total Open Station is packaged for OpenSUSE. Installing is as easy as::

   $ sudo zypper ar http://download.opensuse.org/repositories/Application:/Geo/openSUSE_Leap_15.1/ GEO
   $ sudo zypper refresh
   $ sudo zypper install TotalOpenStation

Change the OpenSUSE version as your wish.

Debian and Ubuntu
-----------------

Total Open Station is included in Debian and Ubuntu, just::

    sudo apt-get install totalopenstation

as usual. Please note that the version provided by your distribution may not
be the latest release.

Mac OSX
=======

Download Python3 from the `official website <https://www.python.org/downloads/mac-osx/>`_,
and follow `this document on the Python.org website <https://www.python.org/download/mac/tcltk/>`_,
that will help you choosing the correct version of Python to use
(Python 3.7.2+, 3.6.8, or 2.7.16+ have builtin Tcl/Tk).

.. warning::

   Do not use the pre-installed Python that comes with the OSX operating system
   which has serious bugs that can cause application crashes.

Microsoft Windows
=================

Two packages need to be installed before the actual installation of
Total Open Station, because the program is written in the Python
programming language which is not installed by default on Windows.

.. warning::

   You might need administrator privileges to be able to install all
   the programs.

Install Python
--------------

Download the latest Python installer for **Python 3**:

- `Python Releases for Windows <https://www.python.org/downloads/windows/>`_

When you've got the installer donwloaded on your computer, install
it. Do not forget to add Python in your PATH and to include pip.
You don’t need to use Python directly, but it is needed for the
program to work.


.. warning::

    As Python 3.5+ are not Windows XP compatible, no support for Windows XP will be available.

Install pySerial
----------------

As with Python, you don’t need to use pySerial directly,
but it is needed for the program to work. |br|
Please make sure you are installing pySerial version 3.4+. |br|
As there is no Windows ready package for pySerial, the best practice is
to install the latest version is to use pip and
the `pySerial PyPI repository <https://pypi.org/project/pyserial/>`_. |br|
Pip in a package manager included in Windows Python3 package
(not by default, you should tick a case) :

    - get a terminal_,
    - then type : ::

        > pip install pyserial


Install Total Open Station
--------------------------

Download the most recent version of Total Open Station from `Github download
<https://github.com/steko/totalopenstation/releases>`_ and install it.

You will find the totalopenstation-gui script in :file:`C:/Python3X/Scripts/`
unless you have changed the standard installation options (not
recommended). You can create a shortcut to the program on your desktop
if you like.

To upgrade to a newer version, just go to the Github download page again
and install it |b|.
The old version will get overwritten. |br|
No data will be lost!


Install the Prolific PL2032 drivers
-----------------------------------

(optional, but recommended).

Most USB-serial adapters are made with the Prolific chipset. If
plugging the cable gives you errors about missing drivers for your
hardware, drivers for Windows can be downloaded from the `Prolific
website <http://www.prolific.com.tw/eng/downloads.asp?ID=31>`_.


Using pip
=========

Until your operating system's packaging tools (e.g. apt or
yum) allow you to install Total Open Station along with other
programs, the recommended way to install is using pip_ (a package
manager for Python) and virtualenv_ (which creates isolated
software environments: basically you don't mix packages installed
system-wise with your package manager and user-installed
software). Here follows a detailed step-by-step guide.

.. _pip: http://www.pip-installer.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv

Install ``pip`` and ``virtualenv``
----------------------------------

First of all, make sure you have ``pip`` and ``virtualenv``
installed. All major GNU/Linux distributions have them packaged:

- Debian and derivatives (including Ubuntu): ``apt-get install
  python-pip python-virtualenv``
- Fedora: ``yum install python-pip python-virtualenv``

For Windows users, pip should be included in your installation
but not virtualenv.
Thus, you need to install it through pip:

    - get a terminal_,
    - then type : ::

        > pip install virtualenv


Create a virtual environment
----------------------------

Creating a virtual environment is as easy as typing in a terminal::

    virtualenv tops-environment

A new directory named ``tops-environment`` was created. It contains a
minimal set of files needed to manage a Python installation that is
isolated from the one installed on your system, helping to keep things
clean.

Now, on GNU/Linux, activate the environment with::

    source tops-environment/bin/activate

or on Windows::

    tops-environment/Scripts/activate.bat

From now on, all Python-related actions will be executed within the
newly created environment, and not on the system-wide
installation. You terminal should look a bit different when the
virtual environment is active::

    (tops-environment)steko@gibreel:$

You can change directory freely, the environment will remain active.

You *deactivate* the environment (that is, you exit from it), with the
``deactivate`` command.

Installing Total Open Station
-----------------------------

Once the virtual environment is *active*, you're ready to install
Total Open Station, with::

    pip install totalopenstation

This will automatically download the latest released version from the
Python Package Index (PyPI), and install all the other required Python
packages as well.

Installing development versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes it is useful to install development versions before they are
released, to help with testing of new features and making sure that
there are no new bugs.

Using the procedure described above it is fairly easy to create
another, separate environment. Once the new environment is *active*,
the command for installing a development version is::

    pip install -e git+https://github.com/steko/totalopenstation#egg=totalopenstation

Developers may ask you to install from another repository, but the
concept stays the same. This mechanism is very flexible and allows to
install and test different versions safely.

Running the program
-------------------

When the program is installed, you can use it from the command line or
with a graphical interface (recommended for new users).

From your terminal, type::

    totalopenstation-gui.py

and the program should start. Please report any errors to the `bug tracker`_.

The next time you want to run the program, follow these steps:

#. open a terminal
#. ``cd`` to the directory where the virtual environment was created
#. ``source tops-environment/bin/activate`` to enter the virtualenv
#. ``totalopenstation-gui.py`` will start the program



.. _terminal:

Get terminal
============

To get the terminal on Windows :

    - open an execute prompt ; Window key + R
    - type cmd and validate

Or

    - open a Windows explorer ; Window key + E
    - Shift + Right click anywhere
    - choose "Open a command prompt here"
