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


usage = "usage: totalopenstation-cli-parser.py [option] arg1 [option] arg2 ..."

parser = OptionParser(usage = usage)
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

(options, args) = parser.parse_args()

if options.informat:
    try:
        exec('from models.%s import ModelParser' % options.informat)
    except ImportError, message:
        from models.models import list_models
        sys.exit("\nError:\n%s\n\n%s" % (message, list_models()))
else:
    sys.exit("Please specify an input format")

if options.outformat:
    try:
        exec('from output.tops_%s import FormatOutput' % options.outformat)
    except ImportError, message:
        sys.exit("\nError:\n%s\n" % message)
else:
    sys.exit("Please specify an output format")


if options.infile:
    if not os.path.exists(options.outfile):
#        e = open(options.outfile, 'w')
#        e.write(result)
#        e.close()
        print "Downloaded data saved to out file %s" % options.outfile
    else:
        sys.exit("Specified output file already exists\n")
else:
    print sys.stdin.read()


#if options.outfile:
#    if not os.path.exists(options.outfile):
#        e = open(options.outfile, 'w')
#        e.write(result)
#        e.close()
#        print "Downloaded data saved to out file %s" % options.outfile
#    else:
#        sys.exit("Specified output file already exists\n")
#else:
#    sys.stdout.write(result)

