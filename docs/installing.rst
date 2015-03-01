.. _installing:

===============================
 Installing Total Open Station
===============================

There are a few different ways to install Total Open Station,
depending on your operating system.

GNU/Linux distributions
=======================

OpenSUSE
--------

Total Open Station is packaged for OpenSUSE. Installing is as easy as::

   $ sudo zypper ar http://download.opensuse.org/repositories/Application:/Geo/openSUSE_12.1/ GEO
   $ sudo zypper refresh
   $ sudo zypper install TotalOpenStation

Debian and Ubuntu
-----------------

Total Open Station is included in Debian and Ubuntu, just::

    sudo apt-get install totalopenstation

as usual. Please note that the version provided by your distribution may not
be the latest release.

Mac OSX
=======

Download Python 2 from the official website, and follow `this document on the
Python.org website <https://www.python.org/download/mac/tcltk/>`_, that will
help you choosing the correct version of Python to use.

.. warning::

   Do not use the pre-installed Python that comes with the OSX operating system.

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

Check whether your Windows is 32 bit (``x86``, common for older versions like
Windows XP) or 64 bit (``x86-64``). Then download the latest Python installer
for **Python 2** (not Python 3):

- `Python Releases for Windows`_

When you've got the installer donwloaded on your computer, install
it. You don’t need to use Python directly, but it is needed for the
program to work.

.. _Python Releases for Windows: https://www.python.org/downloads/windows/

Install pySerial
----------------

Download pySerial_ and install it. As with Python, you don’t need
to use it directly, but it is needed for the program to work. Please make
sure you are installing pySerial version 2.7 or a later version.

.. _pySerial: http://pyserial.sourceforge.net/


Install Total Open Station
--------------------------

Download the most recent version of Total Open Station from `PyPI`_ and install it.
You will find the totalopenstation-gui script in :file:`C:/Python27/Scripts/`
unless you have changed the standard installation options (not
recommended). You can create a shortcut to the program on your desktop
if you like.

To upgrade to a newer version, just go to `PyPI`_ again, download the latest
version and install it as with the first one. The old version will get
overwritten. No data will be lost!

.. _`PyPI`: https://pypi.python.org/pypi/totalopenstation/

Install the Prolific PL2032 drivers
-----------------------------------

(optional, but recommended).

Most USB-serial adapters are made with the Prolific chipset. If
plugging the cable gives you errors about missing drivers for your
hardware, drivers for Windows can be downloaded from the `Prolific
website`_.

.. _`Prolific website`:
   http://www.prolific.com.tw/eng/downloads.asp?ID=31


Using pip (for the latest version)
==================================

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

Create a virtual environment
----------------------------

Creating a virtual environment is as easy as typing in a terminal::

    virtualenv tops-environment

A new directory named ``tops-environment`` was created. It contains a
minimal set of files needed to manage a Python installation that is
isolated from the one installed on your system, helping to keep things
clean.

Now activate the environment with::

    source tops-environment/bin/activate

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

and the program should start. Please report any errors to the `issue tracker`_.

The next time you want to run the program, follow these steps:

#. open a terminal
#. ``cd`` to the directory where the virtual environment was created
#. ``source tops-environment/bin/activate`` to enter the virtualenv
#. ``totalopenstation-gui.py`` will start the program

.. _issue tracker: https://github.com/steko/totalopenstation/issues
