.. _installing:

=============================
Installing Total Open Station
=============================

There are a few different ways to install Total Open Station,
depending on your operating system.

.. note::

    Since version 0.5, Total Open Station is based on Python 3 only. Python 2 is now unsupported.

GNU/Linux distributions
=======================

Installing Total Open Station through your Linux package manager, if available,
is the only way to get automatic updates to the most recent version. All other
installation methods require you to keep track of new releases and manually update.
Total Open Station will not notify you when a new release is available.

To install the latest release, see :ref:`using-pip` below.

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
(Python 3.6.8, 3.7.2 and later have builtin Tcl/Tk).

.. warning::

   Do not use the pre-installed Python that comes with the OSX operating system
   which has serious bugs that can cause application crashes.

Then follow the section :ref:`using-pip` below.

Microsoft Windows
=================

Download the most recent version of Total Open Station from `Github download
<https://github.com/totalopenstation/totalopenstation/releases>`_ and run it.

The Windows version of Total Open Station is portable and everything is
included in the executable, without need to install.

To upgrade to a newer version, just go to the Github download page again.
No data will be lost!

.. warning::
   
   In some cases, there may be a warning about a potential virus
   threat in the downloaded ``.exe`` file. This is a false positive
   and we are actively reaching out to antivirus vendors to make sure
   that Total Open Station is recognized as genuine software. See
   `issue #140`_ for more details.

   On a technical level, the Windows version is created by an
   automated procedure run on GitHub, based solely on the open source
   code of Total Open Station and PyInstaller. See Github Action
   workflow `pyinstaller.yml`_.

.. _`issue #140`: https://github.com/totalopenstation/totalopenstation/issues/140
.. _`pyinstaller.yml`: https://github.com/totalopenstation/totalopenstation/actions/workflows/pyinstaller.yml

Install the Prolific PL2032 drivers
-----------------------------------

(optional, but recommended).

Most USB-serial adapters are made with the Prolific chipset. If
plugging the cable gives you errors about missing drivers for your
hardware, drivers for Windows can be downloaded from the `Prolific
website <http://www.prolific.com.tw/eng/downloads.asp?ID=31>`_.


.. _using-pip:

Using pip
=========

Until your operating system's packaging tools (e.g. apt or
yum) allow you to install Total Open Station along with other
programs, the recommended way to install is using pip_ (a package
manager for Python) and a virtual environment: basically you
don't mix packages installed system-wise with your package manager
and user-installed software). Here follows a detailed step-by-step guide
using a terminal.

.. _pip: http://www.pip-installer.org/

Requirements
------------

You need to have Python installed on your machine. Total Open Station runs
on all supported Python versions (from 3.6 to 3.9).

On Linux, make sure that the ``python3-tk`` or ``python3-tkinter`` package is
installed on your system, otherwise install it with your package manager, for
example on Debian-based systems like Ubuntu::

    sudo apt install python3-tk

or for ArchLinux::

    pacman -S tk

Tkinter is the library used for the graphical interface of Total Open Station.

Create a virtual environment
----------------------------

Creating a virtual environment is as easy as typing in a terminal::

    python3 -m venv tops-environment

A new directory named ``tops-environment`` has been created. It contains a
minimal set of files needed to manage a Python installation that is
isolated from the one installed on your system, helping to keep things
clean.

Now, activate the environment with::

    source tops-environment/bin/activate

(On Windows, this will be tops-environment/Scripts/activate)

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

    pip install -e git+https://github.com/totalopenstation/totalopenstation#egg=totalopenstation

Developers may ask you to install from another repository, but the
concept stays the same. This mechanism is very flexible and allows to
install and test different versions safely.

Running the program
-------------------

When the program is installed, you can use it from the command line or
with a graphical interface (recommended for new users).

From your terminal, type::

    totalopenstation-gui.py

and the program should start.

Of course you can also run the command line programs:

- totalopenstation-cli-connector.py downloads data from your total station
- totalopenstation-cli-parser converts raw data in common formats like DXF and CSV

Please report any errors to the `bug tracker`_.

The next time you want to run the program, follow these steps:

#. open a terminal
#. ``cd`` to the directory where the virtual environment was created
#. ``source tops-environment/bin/activate`` to enter the virtualenv
#. ``totalopenstation-gui.py`` will start the program
