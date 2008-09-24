#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: test_zeiss.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License


from output.dxf.tops_dxf import TotalOpenDXF
from models import zeiss_elta_r55

# read TS data

main = zeiss_elta_r55.ZeissEltaR55('interactive_download.txt')
punti = main.t_points


codici = set([ p[4] for p in punti ])


def make_dxf():
    dxf_output = TotalOpenDXF(punti, 'zeiss.dxf')

make_dxf()

