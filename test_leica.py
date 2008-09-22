#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: prova_leica.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import sys

from output.dxf.tops_dxf import TotalOpenDXF
from output.csv.tops_csv import TotalOpenCSV
from models import leica_tcr_1205

# read TS data

main = leica_tcr_1205.LeicaTCR1205('models/leica_1205_1.txt')
main.parse_retrieve_data()
punti = main.points.list_to_tuple()


def make_dxf():
    dxf_output = TotalOpenDXF(punti, 'leica.dxf')

make_dxf()

def make_csv():
    csv_output = TotalOpenCSV(punti, 'leica.csv')


if len(sys.argv) > 1:
    try:
        eval("make_%s()" % sys.argv[1])
    except NameError:
        print "Output format %s is not recognized" % sys.argv[1]
else:
    print punti[0:30]

