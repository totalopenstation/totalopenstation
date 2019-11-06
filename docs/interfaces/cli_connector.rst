.. _cli-connector:

================================
Total Open Station CLI Connector
================================

This is a command line application to download raw data from total station
devices.

Synopsis
========

totalopenstation-cli-connector.py [options]

Options
=======

  -h, --help            show this help message and exit
  -m MODEL, --model=MODEL
                        select input MODEL
  -p PORT, --port=PORT  select input SERIAL PORT
  -o FILE, --outfile=FILE
                        select output FILE (do not specify for stdout)

Using totalopenstation-cli-connector
------------------------------------

The ``--model`` and ``--port`` options are mandatory.

In most cases the default parameters for serial connection should work, but
you should know how your total station is set, or alternatively you should
be able to set serial parameters on the total station directly.

Output goes to stdout by default, but it is recommended to use the -o option.
