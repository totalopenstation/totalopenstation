#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: totalopenstation-cli-connector.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import sys
import os

from optparse import OptionParser


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

try:
    exec('from totalopenstation.models.%s import ModelConnector' % options.model)
except ImportError, message:
    sys.exit("\nError:\n%s\n" % message)

station = ModelConnector(options.port)
station.open()

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
