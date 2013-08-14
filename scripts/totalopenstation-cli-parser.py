#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: totalopenstation-cli-parser.py
# Copyright 2008-2013 Stefano Costa <steko@iosa.it>

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
import gettext
import importlib

from optparse import OptionParser

from totalopenstation.formats import BUILTIN_INPUT_FORMATS
from totalopenstation.output import BUILTIN_OUTPUT_FORMATS


t = gettext.translation('totalopenstation', './locale', fallback=True)
_ = t.lgettext

usage = _("usage: %prog [option] arg1 [option] arg2 ...")

parser = OptionParser(usage=usage)
parser.add_option("-i",
                "--infile",
                action="store",
                type="string",
                dest="infile",
                help=_("select input FILE  (do not specify for stdin)"),
                metavar="FILE")
parser.add_option("-o",
                "--outfile",
                action="store",
                type="string",
                dest="outfile",
                help=_("select output FILE (do not specify for stdout)"),
                metavar="FILE")
parser.add_option("-f",
                "--input-format",
                action="store",
                type="string",
                dest="informat",
                help=_("select input FORMAT"),
                metavar="FORMAT")
parser.add_option("-t",
                "--output-format",
                action="store",
                type="string",
                dest="outformat",
                help=_("select input FORMAT"),
                metavar="FORMAT")
parser.add_option(
                "--overwrite",
                action="store_true",
                dest="overwrite",
                default=False,
                help=_("overwrite existing output file"))
parser.add_option(
    "--list",
    action="store_true",
    dest="list",
    default=False,
    help=_("list the available input and output formats"))


(options, args) = parser.parse_args()

def list_formats():
    '''Print a list of the supported input and output formats.'''

    from totalopenstation.formats import BUILTIN_INPUT_FORMATS

    mod_string = "List of supported input formats:\n" + "-" * 30 + "\n"
    for k, v in sorted(BUILTIN_INPUT_FORMATS.items()):
        mod_string += k.ljust(20) + v[2] + "\n"
    mod_string += "\n\n"

    mod_string += "List of supported output formats:\n" + "-" * 30 + "\n"
    for k, v in sorted(BUILTIN_OUTPUT_FORMATS.items()):
        mod_string += k.ljust(20) + v[2] + "\n"
    mod_string += "\n"
    return mod_string

if options.list:
    sys.stdout.write(list_formats())
    sys.exit()

def exit_with_error(message):
    sys.exit(_("\nError:\n%(message)s\n\n%(formats)s") % {'message': message,
                                                          'formats': list_formats()})

if options.informat:
    try:
        inputclass = BUILTIN_INPUT_FORMATS[options.informat]
    except KeyError, message:
        exit_with_error(_('%s is not a valid input format') % message)
    else:
        if isinstance(inputclass, tuple):
            try:
                # builtin format parser
                mod, cls, name = inputclass
                inputclass = getattr(importlib.import_module('totalopenstation.formats.' + mod), cls)
            except ImportError, message:
                exit_with_error(message)
else:
    sys.exit(_("Please specify an input format"))

if options.outformat:
    try:
        outputclass = BUILTIN_OUTPUT_FORMATS[options.outformat]
    except KeyError, message:
        exit_with_error('%s is not a valid output format' % message)
    else:
        if isinstance(outputclass, tuple):
            try:
                # builtin output builder
                mod, cls, name = outputclass
                outputclass = getattr(importlib.import_module('totalopenstation.output.' + mod), cls)
            except ImportError, message:
                exit_with_error(message)

if options.infile:
    infile = open(options.infile, 'r').read()
else:
    if sys.stdin.isatty():
        sys.exit(_('No input data!'))
    else:
        infile = sys.stdin.read()


def main(infile):
    '''After setting up all parameters, finally try to process input data.'''

    parsed_data = inputclass(infile)
    parsed_points = parsed_data.points
    output = outputclass(parsed_points)

    def write_to_file(outfile):
        e = open(outfile, 'w')
        e.write(output.process())
        e.close()

    if options.outfile:
        if not os.path.exists(options.outfile):
            write_to_file(options.outfile)
            print _("Downloaded data saved to out file %s") % options.outfile
        else:
            if options.overwrite:
                write_to_file(options.outfile)
                print _("Downloaded data saved to file %s,") % options.outfile,
                print _("overwriting the existing file")
            else:
                sys.exit(_("Specified output file already exists\n"))
    else:
        sys.stdout.write(output.process())

if __name__ == '__main__':
    main(infile)
