.. _installing:

===============================
 Installing Total Open Station
===============================

There are a few different ways to install Total Open Station,
depending on your operating system. If you are on GNU/Linux or Mac
OSX, you should already have Python installed on your
system.

Instructions for Microsoft Windows are at the end of this page.

GNU/Linux distributions
=======================

OpenSUSE
--------

Total Open Station is packaged for OpenSUSE. Installing is as easy as::

   $ sudo zypper ar http://download.opensuse.org/repositories/Application:/Geo/openSUSE_12.1/ GEO
   $ sudo zypper refresh
   $ sudo zypper install TotalOpenStation


Using pip (recommended)
=======================

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

    pip install -e hg+https://bitbucket.org/steko/totalopenstation#egg=totalopenstation

Developers may ask you to install from another repository, but the
concept stays the same. This mechanism is very flexible and allows to
install and test different versions safely.

Running the program
-------------------

When the program is installed, you can use it from the command line or
with a graphical interface (recommended for new users).

From your terminal, type::

    totalopenstation-gui.py

and the program should start. Please report any errors to the `mailing
list`_

The next time you want to run the program, follow these steps:

#. open a terminal
#. ``cd`` to the directory where the virtual environment was created
#. ``source tops-environment/bin/activate`` to enter the virtualenv
#. ``totalopenstation-gui.py`` will start the program

.. _`mailing list`: https://lists.berlios.de/mailman/listinfo/tops-dev

Microsoft Windows
=================

Three packages need to be installed before the actual installation of
Total Open Station, because the program is written in the Python
programming language which is not installed by default on Windows.

.. warning::

   You might need administrator privileges to be able to install all
   the programs.

Install Python
--------------

Check whether your Windows is 32 bit (common) or 64 bit. Then download
the right Python installer (direct link to the installation download):

- `32-bit Python installer`_
- `64-bit Python installer`_

When you've got the installer donwloaded on your computer, install
it. You don’t need to use Python directly, but it is needed for the
program to work.

.. _`32-bit Python installer`: http://python.org/ftp/python/2.7.2/python-2.7.2.msi
.. _`64-bit Python installer`: http://python.org/ftp/python/2.7.2/python-2.7.2.amd64.msi

Install PythonWin
-----------------

Download PythonWin_ from and install it. Again, you don’t
need to use it directly, but it is needed for the program to work.

Be sure to choose the right version, that is, the one that matches
your operating system (either 32 bit or 64 bit) and your Python
version (2.7 if you followed the above steps).

.. _PythonWin: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20217/

Install pySerial
----------------

Download pySerial_ and install it. As with PythonWin, you don’t need
to use it directly, but it is needed for the program to work. Do NOT
install pySerial 2.5 because it doesn’t work correctly on Windows.

.. _pySerial: http://sourceforge.net/projects/pyserial/files/pyserial/2.4/pyserial-2.4.win32.exe/download


Install Total Open Station
--------------------------

Download the most recent version of `Total Open Station`_ and install it.
You will find the totalopenstation-gui script in C:/Python27/Scripts/
unless you have changed the standard installation options (not
recommended). You can create a shortcut to the program on your desktop
if you like.

To upgrade to a newer version, just go to
http://pypi.python.org/pypi/totalopenstation, download the latest
version and install it as with the first one. The old version will get
overwritten. No data will be lost!

.. _`Total Open Station`: http://pypi.python.org/packages/any/t/totalopenstation/totalopenstation-0.3.linux-x86_64.exe#md5=85f144de2e06e6fffc7c6d1fac095167


Install the Prolific PL2032 drivers
-----------------------------------

(optional, but recommended).

Most USB-serial adapters are made with the Prolific chipset. If
plugging the cable gives you errors about missing drivers for your
hardware, drivers for Windows can be downloaded from the `Prolific
website`_.

.. _`Prolific website`:
   http://www.prolific.com.tw/eng/downloads.asp?ID=31

Running the program
-------------------

Total Open Station will be installed at
:file:`C:/Python27/Scripts/totalopenstation-gui.py`. Double-click on this
file to start the program. You can create a shortcut if you want. We
are still working on providing an installer that will do it for you.
