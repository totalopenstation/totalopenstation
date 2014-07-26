#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: totalopenstation-cli-connector.py
# Copyright 2008,2011 Stefano Costa <steko@iosa.it>

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

from totalopenstation.models import BUILTIN_MODELS

usage = "usage: %prog [option] arg1 [option] arg2 ..."

parser = OptionParser(usage=usage)
parser.add_option("-m",
                "--model",
                action="store",
                type="string",
                dest="model",
                help="select input MODEL",
                metavar="MODEL")
parser.add_option("-p",
                "--port",
                action="store",
                type="string",
                dest="port",
                help="select input SERIAL PORT",
                metavar="PORT")
parser.add_option("-o",
                "--outfile",
                action="store",
                type="string",
                dest="outfile",
                help="select output FILE (do not specify for stdout)",
                metavar="FILE")

(options, args) = parser.parse_args()

if not (options.model and options.port):
    sys.exit("Please specify your model and the port to download from")

modelclass = BUILTIN_MODELS[options.model]

# import input format parser
if isinstance(modelclass, tuple):
    try:
        # builtin format parser
        mod, cls, name = modelclass
        modelclass = getattr(
            __import__('totalopenstation.models.' + mod, None, None, [cls]), cls)
    except ImportError, msg:
        sys.exit(_('Error loading the required model module: %s' % msg))

station = modelclass(options.port)
try:
    station.close()  # sometimes the port will be already open for no reason
    station.open()
except serial.SerialException, detail:
    sys.exit(detail)

print "Now you can start download from %s device" % options.model

station.start()
station.dl_started.wait()
print "Download started..."
station.dl_finished.wait()
print "Download finished..."
result = station.result

if options.outfile:
    if not os.path.exists(options.outfile):
        e = open(options.outfile, 'w')
        e.write(result)
        e.close()
        print "Downloaded data saved to out file %s" % options.outfile
    else:
        sys.exit("Specified output file already exists\n")
else:
    sys.stdout.write(result)
