#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: totalopenstation-cli-parser.py
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>

# This file is part of Total Open Station.

# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.

import sys
import os

from optparse import OptionParser

usage = "usage: %prog [option] arg1 [option] arg2 ..."

parser = OptionParser(usage=usage)
parser.add_option("-i",
                "--infile",
                action="store",
                type="string",
                dest="infile",
                help="select input FILE  (do not specify for stdin)",
                metavar="FILE")
parser.add_option("-o",
                "--outfile",
                action="store",
                type="string",
                dest="outfile",
                help="select output FILE (do not specify for stdout)",
                metavar="FILE")
parser.add_option("-f",
                "--input-format",
                action="store",
                type="string",
                dest="informat",
                help="select input FORMAT",
                metavar="FORMAT")
parser.add_option("-t",
                "--output-format",
                action="store",
                type="string",
                dest="outformat",
                help="select input FORMAT",
                metavar="FORMAT")
parser.add_option(
                "--overwrite",
                action="store_true",
                dest="overwrite",
                default=False,
                help="overwrite existing output file")

(options, args) = parser.parse_args()

if options.informat:
    try:
        iformat = __import__('totalopenstation.formats.%s' % options.informat,
                             globals(),
                             locals(),
                             ['FormatParser'])
    except ImportError, message:
        from totalopenstation.formats.formats import list_formats
        sys.exit("\nError:\n%s\n\n%s" % (message, list_formats()))
else:
    sys.exit("Please specify an input format")

if options.outformat:
    try:
        name = 'totalopenstation.output.tops_%s' % options.outformat
        oformat = __import__(name,
                             globals(),
                             locals(),
                             ['OutputFormat'])
    except ImportError, message:
        sys.exit("\nError:\n%s\n" % message)
else:
    sys.exit("Please specify an output format")


if options.infile:
    infile = open(options.infile, 'r').read()
else:
    infile = sys.stdin.read()


def main(infile):
    '''After setting up all parameters, finally try to process input data.'''

    parsed_data = iformat.FormatParser(infile)
    parsed_points = parsed_data.points
    output = oformat.OutputFormat(parsed_points)

    def write_to_file(outfile):
        e = open(outfile, 'w')
        e.write(output.process())
        e.close()

    if options.outfile:
        if not os.path.exists(options.outfile):
            write_to_file(options.outfile)
            print "Downloaded data saved to out file %s" % options.outfile
        else:
            if options.overwrite:
                write_to_file(options.outfile)
                print "Downloaded data saved to file %s," % options.outfile,
                print "overwriting the existing file"
            else:
                sys.exit("Specified output file already exists\n")
    else:
        sys.stdout.write(output.process())

if __name__ == '__main__':
    main(infile)
