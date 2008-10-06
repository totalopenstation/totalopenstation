#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: test_zeiss.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import sys

from output.dxf.tops_dxf import TotalOpenDXF
from output.dat.tops_dat import TotalOpenDAT
from models import zeiss_elta_r55

# read TS data

main = zeiss_elta_r55.ModelParser('interactive_download.txt')
punti = main.t_points


codici = set([ p[4] for p in punti ])


def make_dxf():
    dxf_output = TotalOpenDXF(punti, 'zeiss.dxf')

def make_dat():
    dat_output = TotalOpenDAT(punti, 'zeiss.dat')


if len(sys.argv) > 1:
    try:
        eval("make_%s()" % sys.argv[1])
    except NameError:
        print "Output format %s is not recognized" % sys.argv[1]

