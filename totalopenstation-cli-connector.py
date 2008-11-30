#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: interactive.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import sys

from optparse import OptionParser

from models import *


usage = "usage: totalopenstation-cli-connector.py [option] arg1 [option] arg2 ..."

parser = OptionParser(usage = usage)
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

exec('from models.%s import ModelConnector' % options.model)

station = ModelConnector(options.port)
station.open()

print "Start download from %s device" % options.model

result = station.fast_download()

if options.outfile:
    e = open(options.outfile, 'w')
    e.write(result)
    e.close()
    print "Downloaded data saved to out file %s" % options.outfile
else:
    sys.stdout.write(result)

