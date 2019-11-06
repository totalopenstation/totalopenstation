.. _cli-parser:

=============================
Total Open Station CLI Parser
=============================

This is a command line application to convert raw data to common formats for
use in CAD or GIS environments.

Synopsis
========

totalopenstation-cli-parser [options]

Options
=======

  -h, --help            show this help message and exit
  -i FILE, --infile=FILE
                        select input FILE  (do not specify for stdin)
  -o FILE, --outfile=FILE
                        select output FILE (do not specify for stdout)
  -f FORMAT, --input-format=FORMAT
                        select input FORMAT
  --2d                  Exclude Z coordinates, output only 2D data
  -t FORMAT, --output-format=FORMAT
                        select input FORMAT
  -r, --raw             Enhanced parsed file process
  --overwrite           overwrite existing output file
  --list                list the available input and output formats

Using totalopenstation-cli-parser
---------------------------------

If no input file is specified, input is read from stdin.

Output goes to stdout by default, but it is recommended to use the -o option.

Raw parsing
-----------

The ``--raw`` option is useful when exporting to CSV for processing in
other programs, and will export all field records found in the raw data from
the total station. It only makes sense for certain input formats where the
original measurements are stored, namely:

- Leica GSI
- Nikon RAW
- Carlson RW5
