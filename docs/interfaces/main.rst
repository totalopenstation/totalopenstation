.. _interfaces:

========================
Using Total Open Station
========================

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

A complete manual of :ref:`gui-main`


Command-line
============

After :ref:`installing`, there will be three new executable programs
in your path. Two of them are meant for being run in a terminal, and
are extremely useful for batch operations and easy repeating of common
tasks with minimum time effort.

:ref:`cli-connector` and :ref:`cli-parser`
are two command line programs that make the same features of the graphical
interface available to those who prefer working in a terminal. They are well
documented, and they make it possible to process large amounts of data files
via shell scripting, or to drastically reduce the time needed for downloading
raw data.

These two programs also provide a basic but complete example of how to
use Total Open Station as a programming library.


.. toctree::
  :maxdepth: 1

  cli_connector
  cli_parser
  gui_main
