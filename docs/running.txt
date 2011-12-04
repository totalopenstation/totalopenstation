.. _running:

==========================
 Using Total Open Station
==========================

There are two ways to use Total Open Station, from the command line or
as a user-friendly program. Each mode of operation has its drawbacks,
and both are constantly used and tested.

Graphical User Interface
========================

If you followed the guide about :ref:`installing`, you should be able
to start Total Open Station.

The basic usage of Total Open Station is made of the following steps:

#. download raw data from the total station
#. save raw data (optional, but recommended)
#. export raw data to an output format

Saving raw data enables you to open data files even at a later stage
and process them when it's more appropriate.

Downloading raw data
--------------------

To download raw data, your total station must be connected to the
computer you are using, and the connection parameters must be known
and set in the program. Total Open Station saves certain parameters
across work sessions, but not all of them are saved, yet.

The normal download procedure is a four-step operation:

#. once the right parameters are set, click on the :guilabel:`Connect`
   button
#. a small window appears, telling that the program is ready to start
   the download
#. start the data transfer from the menu of the total station
#. press the :guilabel:`OK` button in the small window (the order of
   these two last steps matters)

Downloaded data will be shown in real-time in the main program
window. A short information dialog will appear at the end of the
transfer. If any error blocks you in this procedure, please send a
detailed description to the mailing list so we can help you.

Saving raw data
---------------

Raw data shown in the main program window can be edited if you need,
and saved to disk clicking the :guilabel:`Save raw data` button. We
highly recommend to save all data to disk before any other action,
because it prevents data loss and it is a very convenient way to have
a backup of your work. Plus, raw data files are generally very small
in size if compared to the exported files.

By default saved files get a :file:`.tops` extension, but it is
absolutely optional to have this extension.

Opening previously saved data
-----------------------------

The :guilabel:`Open file` button lets you open any ASCII file you have on
your disk for processing with Total Open Station, either previously
saved with TOPS itself or not.

Data can be edited in the text area. Editing patterns include:

- removing lines of data that don't need to be processed
- correcting errors in data
- pasting more than one data file together

Please note that if you do not know well the raw data format you are
editing, data may become inconsistent, and it will not be possible to
process them properly later. If you are unsure, do not edit raw data.

Exporting data
--------------

The main purpose of Total Open Station is to export raw data in
formats that are not read by GIS and CAD programs, to common formats
that are easy to import.

To start exporting data, make sure that the text area in the main
program window contains the data you want to export. If this is not
the case, you can either download data from your total station or open
a previously-saved data file.

Click the :guilabel:`Process data` button. A window will appear,
allowing you to choose two processing options:

- the input format
- the output format

Select the input format of the raw data you have (if you are using the
same total station all the time, it will be probably the same -- we
are working on adding a way to save the last used formats across
different working sessions).

Then select the output format you want to use, and proceed with the
:guilabel:`OK` button. You will be asked where you want to save the
exported file.

You can now open your exported data in the GIS or CAD program of
choice for further processing. Should you need to go back to the
original data, you can always repeat the above procedure starting from
the saved raw data file.

Command-line
============

After :ref:`installing`, there will be three new executable programs
in your path. Two of them are meant for being run in a terminal, and
are extremely useful for batch operations and easy repeating of common
tasks with minimum time effort.

:program:`totalopenstation-cli-connector` and
:program:`totalopenstation-cli-parser` are two command line programs
that make the same features of the graphical interface available to
those who prefer working in a terminal. They are well documented, and
they make it possible to process large amounts of data files via shell
scripting, or to drastically reduce the time needed for downloading
raw data.

These two programs also provide a basic but complete example of how to
use Total Open Station as a programming library.
